--MaxCompute SQL
--********************************************************************--
--author: 蔡圣哲
--create time: 2025-12-02 11:41:22
--********************************************************************--
SET odps.sql.hive.compatible = true
;
-- DROP TABLE IF EXISTS tapdb_one_data.dws_torchlight_s13gameplay_df;


CREATE TABLE IF NOT EXISTS tapdb_one_data.dws_torchlight_s13gameplay_df
(
    account                       STRING COMMENT '用户ID'
    ,season                       BIGINT COMMENT '赛季'
    ,s13_craving_substance_cnt    BIGINT COMMENT '01 累计获得渴瘾物质数量 (coin_id=Coin_826)'
    ,s13_perfect_organ_cnt        BIGINT COMMENT '02 累计掉落完美器官数量 (item_id 381001~381083)'
    ,s13_scavenger_kill_cnt       BIGINT COMMENT '03 累计击杀清道夫数量 (cfgid 1220108/1220701/1220703/1220704)'
    ,s13_level_open_cnt           BIGINT COMMENT '04 终局玩法开启总次数'
    ,s13_level_score_max          BIGINT COMMENT '05 终局玩法单局最高分'
    ,s13_level_score_min          BIGINT COMMENT '06 终局玩法单局最低分'
    ,s13_colored_jar_cnt          BIGINT COMMENT '07 累积开启彩色罐子数 (rarity=7)'
    ,s13_max_monster_num          BIGINT COMMENT '08 终局玩法单局养成怪物最多数量'
    ,s13_max_single_monster_score BIGINT COMMENT '09 终局玩法养成最高单个怪物分'
    ,s13_most_used_modifier       BIGINT COMMENT '10 选择次数最多的手术用具 card_modifier'
    ,s13_most_used_effect         BIGINT COMMENT '11 选择次数最多的药剂 card_effect'
    ,s13_total_vitality           BIGINT COMMENT '12 赛季内累计获得的总活性 gameplay_score SUM'
)
COMMENT 'S13赛季终局玩法用户行为汇总宽表 每日全量'
PARTITIONED BY
(
    dt                        STRING COMMENT '业务日期, yyyy-mm-dd'
)
STORED AS ALIORC
TBLPROPERTIES ('columnar.nested.type' = 'true')
LIFECYCLE 3650
;



-- ================================================================
--   01. 累计获得渴瘾物质数量       dwd_torchlight_coin_ri          coin_id='Coin_826'
--   02. 累计掉落完美器官数量       dwd_torchlight_item_di          item_id 381001~381083
--   03. 累计击杀清道夫数量         dwd_torchlight_battle_di        battle_leave.monster_die_by_id cfgid 1220108/1220701/1220703/1220704
--   04. 终局玩法开启总次数         dwd_torchlight_s13gameplay_level_di   s13gameplay_level_begin
--   05. 终局玩法单局最高分         dwd_torchlight_s13gameplay_level_di   s13gameplay_level_finish.score_actual MAX
--   06. 终局玩法单局最低分         dwd_torchlight_s13gameplay_level_di   s13gameplay_level_finish.score_actual MIN
--   07. 累积开启彩色罐子           dwd_torchlight_s13gameplay_level_di   s13gameplay_level_finish.reward_infos rarity=7
--   08. 终局玩法养成最多怪物数量   dwd_torchlight_s13gameplay_plague_di  s13gameplay_plague_finish.monster_info[].num 单局 SUM MAX
--   09. 终局玩法养成最高单个怪物分 dwd_torchlight_s13gameplay_plague_di  s13gameplay_plague_finish.monster_info[].score MAX
--   10. 选择次数最多的手术用具     dwd_torchlight_s13gameplay_plague_di  s13gameplay_plague_round_end.card_modifier MODE
--   11. 选择次数最多的药剂         dwd_torchlight_s13gameplay_plague_di  s13gameplay_plague_round_end.card_effect   MODE
--   12. 赛季内累计获得的总活性     dwd_torchlight_s13gameplay_plague_di  s13gameplay_plague_finish.gameplay_score   SUM
-- ================================================================
WITH

-- ----------------------------------------------------------------
-- BASE 01: 终局表 —— 两个事件一次扫描
--   04. level_begin  → 开启次数
--   05. level_finish → score_actual MAX
--   06. level_finish → score_actual MIN
--   07. level_finish → reward_infos（彩色宝箱）
-- ----------------------------------------------------------------
cte_level AS (
    SELECT
        account,
        season,
        COUNT(CASE WHEN name = 's13gameplay_level_begin'              THEN 1 END) AS level_open_cnt,
        MAX(CASE  WHEN name = 's13gameplay_level_finish' THEN score_actual END)   AS level_score_max,
        MIN(CASE  WHEN name = 's13gameplay_level_finish' THEN score_actual END)   AS level_score_min
    FROM tapdb_one_data.dwd_torchlight_s13gameplay_level_di
    WHERE dt BETWEEN '2026-01-17' AND '${dt}'
    GROUP BY account, season
),

-- 07. 从 level_finish 的 reward_infos 里展开宝箱，彩色 = rarity = 7
--   reward_infos 是 ARRAY<STRING>，每个元素是 JSON 字符串如 '{"rarity":7,...}'
--   用 EXPLODE 展开后再 GET_JSON_OBJECT 取字段
cte_reward_raw AS (
    SELECT
        account,
        season,
        CAST(GET_JSON_OBJECT(box_json, '$.rarity') AS BIGINT) AS box_rarity
    FROM tapdb_one_data.dwd_torchlight_s13gameplay_level_di
    LATERAL VIEW EXPLODE(reward_infos) tmp AS box_json
    WHERE name         = 's13gameplay_level_finish'
      AND dt BETWEEN '2026-01-17' AND '${dt}'
      AND reward_infos IS NOT NULL
      AND SIZE(reward_infos) > 0
),

cte_colored_jar AS (
    SELECT
        account,
        season,
        COUNT(CASE WHEN box_rarity = 4 THEN 1 END) AS colored_jar_cnt
    FROM cte_reward_raw
    GROUP BY account, season
),

-- ----------------------------------------------------------------
-- BASE 02: plague 表 finish 事件 —— 一次扫描，供 08/09/12 复用
--   12. gameplay_score SUM
--   08/09. monster_info 展开
-- ----------------------------------------------------------------
cte_plague_finish AS (
    SELECT
        account,
        season,
        round_unique_id,
        gameplay_score,
        monster_info,
        card_effect_list,
        card_relic_list
    FROM tapdb_one_data.dwd_torchlight_s13gameplay_plague_di
    WHERE name   = 's13gameplay_plague_finish'
      AND dt BETWEEN '2026-01-17' AND '${dt}'
),

-- 12. 赛季内累计获得的总活性 = 每局 plague 结束分数加总
cte_vitality AS (
    SELECT
        account,
        season,
        SUM(gameplay_score) AS total_vitality
    FROM cte_plague_finish
    GROUP BY account, season
),

-- 08/09. 展开 monster_info 数组，每行一个怪物
--   monster_info 是 ARRAY<STRING>，每个元素是 JSON 字符串如 '{"id":1,"num":10,"score":20}'
--   用 EXPLODE 展开后再 GET_JSON_OBJECT 取字段
cte_plague_monster_raw AS (
    SELECT
        account,
        season,
        round_unique_id,
        CAST(GET_JSON_OBJECT(monster_json, '$.num')   AS BIGINT) AS monster_num,
        CAST(GET_JSON_OBJECT(monster_json, '$.score') AS BIGINT) AS monster_score
    FROM cte_plague_finish
    LATERAL VIEW EXPLODE(monster_info) tmp AS monster_json
    WHERE monster_info IS NOT NULL
      AND SIZE(monster_info) > 0
),

-- 08. 每局养成怪物总数 → 取账号赛季内单局最大值
cte_monster_per_round AS (
    SELECT
        account,
        season,
        round_unique_id,
        SUM(monster_num) AS round_monster_total
    FROM cte_plague_monster_raw
    GROUP BY account, season, round_unique_id
),

cte_plague_monster AS (
    SELECT
        account,
        season,
        MAX(round_monster_total) AS max_monster_num
    FROM cte_monster_per_round
    GROUP BY account, season
),

-- 09. 账号赛季内所有局中最高单个怪物分数
cte_plague_monster_score AS (
    SELECT
        account,
        season,
        MAX(monster_score) AS max_single_monster_score
    FROM cte_plague_monster_raw
    GROUP BY account, season
),

-- ----------------------------------------------------------------
-- BASE 03: 展开 card_relic_list / card_effect_list（来自 plague_finish）
--   10. card_relic_list  → 手术用具（遗物牌）选择次数最多的 id
--   11. card_effect_list → 药剂（效果牌）选择次数最多的 id
-- ----------------------------------------------------------------
cte_relic_raw AS (
    SELECT
        account,
        season,
        CAST(relic_card AS BIGINT) AS relic_card
    FROM cte_plague_finish
    LATERAL VIEW EXPLODE(card_relic_list) t AS relic_card
    WHERE card_relic_list IS NOT NULL
      AND SIZE(card_relic_list) > 0
),

-- 10. 手术用具：赛季内选择次数最多的遗物牌
cte_top_modifier AS (
    SELECT account, season, relic_card AS most_used_modifier
    FROM (
        SELECT
            account,
            season,
            relic_card,
            ROW_NUMBER() OVER (PARTITION BY account, season ORDER BY cnt DESC) AS rn
        FROM (
            SELECT account, season, relic_card, COUNT(1) AS cnt
            FROM cte_relic_raw
            GROUP BY account, season, relic_card
        ) t
    ) t2
    WHERE rn = 1
),

cte_effect_raw AS (
    SELECT
        account,
        season,
        CAST(effect_card AS BIGINT) AS effect_card
    FROM cte_plague_finish
    LATERAL VIEW EXPLODE(card_effect_list) t AS effect_card
    WHERE card_effect_list IS NOT NULL
      AND SIZE(card_effect_list) > 0
),

-- 11. 药剂：赛季内选择次数最多的效果牌
cte_top_effect AS (
    SELECT account, season, effect_card AS most_used_effect
    FROM (
        SELECT
            account,
            season,
            effect_card,
            ROW_NUMBER() OVER (PARTITION BY account, season ORDER BY cnt DESC) AS rn
        FROM (
            SELECT account, season, effect_card, COUNT(1) AS cnt
            FROM cte_effect_raw
            GROUP BY account, season, effect_card
        ) t
    ) t2
    WHERE rn = 1
),

-- ----------------------------------------------------------------
-- CTE 04: 渴瘾物质 —— coin_id = 'Coin_826'
--   01. 渴瘾物质  coin_id = 'Coin_826'
-- ----------------------------------------------------------------
cte_craving AS (
    SELECT
        account,
        season,
        SUM(coin_change_count) AS craving_substance_cnt
    FROM tapdb_one_data.dwd_torchlight_coin_ri
    WHERE coin_id = 'Coin_826'
      AND dt BETWEEN '2026-01-17' AND '${dt}'
    GROUP BY account, season
),

-- ----------------------------------------------------------------
-- CTE 05: 道具流水 —— 完美器官
--   02. 完美器官  item_id BETWEEN 381001 AND 381083
-- ----------------------------------------------------------------
cte_item AS (
    SELECT
        account,
        season,
        SUM(item_change_count) AS perfect_organ_cnt
    FROM tapdb_one_data.dwd_torchlight_item_di
    WHERE name   = 'item_income'
      AND dt BETWEEN '2026-01-17' AND '${dt}'
      AND item_id BETWEEN 381001 AND 381083
    GROUP BY account, season
),

-- ----------------------------------------------------------------
-- CTE 06: 战斗流水 - 清道夫击杀数
--   battle_leave.monster_die_by_id JSON 格式 {"cfgid": 击杀数, ...}
--   清道夫 cfgid: 1220108 / 1220701 / 1220703 / 1220704
-- ----------------------------------------------------------------
cte_scavenger AS (
    SELECT
        account,
        season,
        SUM(
            COALESCE(CAST(GET_JSON_OBJECT(monster_die_by_id, '$.1220108') AS BIGINT), 0)
          + COALESCE(CAST(GET_JSON_OBJECT(monster_die_by_id, '$.1220701') AS BIGINT), 0)
          + COALESCE(CAST(GET_JSON_OBJECT(monster_die_by_id, '$.1220703') AS BIGINT), 0)
          + COALESCE(CAST(GET_JSON_OBJECT(monster_die_by_id, '$.1220704') AS BIGINT), 0)
        ) AS scavenger_kill_cnt
    FROM tapdb_one_data.dwd_torchlight_battle_di
    WHERE name              = 'battle_leave'
      AND dt BETWEEN '2026-01-17' AND '${dt}'
      AND monster_die_by_id IS NOT NULL
    GROUP BY account, season
),

-- ----------------------------------------------------------------
-- UNION: 收集所有数据源中出现过的 account + season（避免 FULL OUTER JOIN 链）
-- ----------------------------------------------------------------
cte_all_accounts AS (
    SELECT account, season FROM cte_level
    UNION SELECT account, season FROM cte_craving
    UNION SELECT account, season FROM cte_item
    UNION SELECT account, season FROM cte_scavenger
    UNION SELECT account, season FROM cte_vitality
    UNION SELECT account, season FROM cte_plague_monster
    UNION SELECT account, season FROM cte_plague_monster_score
    UNION SELECT account, season FROM cte_top_modifier
    UNION SELECT account, season FROM cte_top_effect
    UNION SELECT account, season FROM cte_colored_jar
)

-- ================================================================
-- 最终汇总：以 all_accounts 为基准，所有指标 LEFT JOIN
-- ================================================================
INSERT OVERWRITE TABLE tapdb_one_data.dws_torchlight_s13gameplay_df PARTITION (dt = '${dt}')

SELECT
    ar.account,
    ar.season,

    COALESCE(cr.craving_substance_cnt,     0) AS s13_craving_substance_cnt,     -- 01 累计获得渴瘾物质数量
    COALESCE(it.perfect_organ_cnt,         0) AS s13_perfect_organ_cnt,         -- 02 累计掉落完美器官数量
    COALESCE(sc.scavenger_kill_cnt,        0) AS s13_scavenger_kill_cnt,        -- 03 累计击杀清道夫数量
    COALESCE(lv.level_open_cnt,            0) AS s13_level_open_cnt,            -- 04 终局玩法开启总次数
    COALESCE(lv.level_score_max,           0) AS s13_level_score_max,           -- 05 终局玩法单局最高分
    COALESCE(lv.level_score_min,           0) AS s13_level_score_min,           -- 06 终局玩法单局最低分
    COALESCE(cj.colored_jar_cnt,           0) AS s13_colored_jar_cnt,           -- 07 累积开启彩色罐子
    COALESCE(pm.max_monster_num,           0) AS s13_max_monster_num,           -- 08 终局玩法养成最多怪物数量
    COALESCE(ps.max_single_monster_score,  0) AS s13_max_single_monster_score,  -- 09 终局玩法养成最高单个怪物分数
    tm.most_used_modifier                     AS s13_most_used_modifier,        -- 10 选择次数最多的手术用具
    te.most_used_effect                       AS s13_most_used_effect,          -- 11 选择次数最多的药剂
    COALESCE(vi.total_vitality,            0) AS s13_total_vitality             -- 12 赛季内累计获得的总活性

FROM                 cte_all_accounts       ar
LEFT JOIN            cte_level              lv ON ar.account = lv.account AND ar.season = lv.season
LEFT JOIN            cte_craving            cr ON ar.account = cr.account AND ar.season = cr.season
LEFT JOIN            cte_item               it ON ar.account = it.account AND ar.season = it.season
LEFT JOIN            cte_scavenger          sc ON ar.account = sc.account AND ar.season = sc.season
LEFT JOIN            cte_vitality           vi ON ar.account = vi.account AND ar.season = vi.season
LEFT JOIN            cte_plague_monster     pm ON ar.account = pm.account AND ar.season = pm.season
LEFT JOIN            cte_plague_monster_score ps ON ar.account = ps.account AND ar.season = ps.season
LEFT JOIN            cte_top_modifier       tm ON ar.account = tm.account AND ar.season = tm.season
LEFT JOIN            cte_top_effect         te ON ar.account = te.account AND ar.season = te.season
LEFT JOIN            cte_colored_jar        cj ON ar.account = cj.account AND ar.season = cj.season
;


-- SELECT  *
-- FROM    tapdb_one_data.dws_torchlight_s13gameplay_df
--  WHERE dt = '2026-03-19'
-- and account = '485817723600031745'
-- ;
