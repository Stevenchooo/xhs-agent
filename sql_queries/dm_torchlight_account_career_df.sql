--odps sql
--********************************************************************--
--author:蔡圣哲
--create time:2023-05-31 17:33:48
--********************************************************************--
USE tapdb_one_data
;

-- ALTER TABLE temp_dws_torchlight_account_career_df RENAME TO dm_torchlight_account_career_df;
CREATE TABLE IF NOT EXISTS tapdb_one_data.dm_torchlight_account_career_df
(
    account                                  STRING COMMENT '平台ID'
    ,season                                  INT COMMENT '赛季'
    ,totl_login_days                         BIGINT COMMENT '总活跃天数'
    ,totl_play_sec                           BIGINT COMMENT '累计游戏时长'
    ,sesn_login_days                         BIGINT COMMENT '赛季活跃天数'
    ,sesn_play_sec                           BIGINT COMMENT '赛季游戏时长'
    ,totl_killed_amt                         BIGINT COMMENT '累计怪物击杀数量'
    ,highest_hero_purchase_level             BIGINT COMMENT '最高英雄专精等级'
    ,dungeon_complete_times                  BIGINT COMMENT '通关异界关卡次数'
    ,dungeon_plane_watcher_killed_times      BIGINT COMMENT '击败位面监视者（任意难度）次数'
    ,dungeon_realm_lord_killed_times         BIGINT COMMENT '击败万界之主（任意难度：指时刻678）次数'
    ,dungeon_keegan_and_pirates_killed_times BIGINT COMMENT '击败基冈、男海盗（任意难度：34令，123函）次数'
    ,gow_open_times                          BIGINT COMMENT '征战之神开启次数'
    ,gop_open_times                          BIGINT COMMENT '巨力之神开启次数'
    ,goh_open_times                          BIGINT COMMENT '狩猎之神开启次数'
    ,gom_open_times                          BIGINT COMMENT '机械之神开启次数'
    ,flame_elementium_aqr_amt                BIGINT COMMENT '初火源质获得数量'
    ,flame_sand_aqr_amt                      BIGINT COMMENT '初火灵砂获得数量'
    ,flame_dust_aqr_amt                      BIGINT COMMENT '初火微尘获得数量'
    ,ember_aqr_amt                           BIGINT COMMENT '所有灰烬获得数量'
    ,flame_elementium_craft_cnsum_amt        BIGINT COMMENT '初火源质打造消耗数量'
    ,flame_sand_craft_cnsum_amt              BIGINT COMMENT '初火灵砂打造消耗数量'
    ,flame_dust_craft_cnsum_amt              BIGINT COMMENT '初火微尘打造消耗数量'
    ,ember_craft_cnsum_amt                   BIGINT COMMENT '所有灰烬打造消耗数量'
    ,flame_elementium_aqr_maximum_day_amt    BIGINT COMMENT '单日初火源质最高获取数量'
    ,fluorescent_memory_aqr_amt              BIGINT COMMENT '记忆荧光获取数量'
    ,compass_aqr_amt                         BIGINT COMMENT '罗盘获取数量'
    ,legendary_gear_aqr_amt                  BIGINT COMMENT '暗金装备拾取数量'
    ,other_gear_aqr_amt                      BIGINT COMMENT '其他装备拾取数量'
    ,alevel_legendary_gear_aqr_amt           BIGINT COMMENT 'A级暗金装备获得数量'
    ,blevel_legendary_gear_aqr_amt           BIGINT COMMENT 'B级暗金装备获得数量'
    ,gear_corroded_times                     BIGINT COMMENT '装备侵蚀次数'
    ,gear_defiled_times                      BIGINT COMMENT '装备侵蚀获得【亵渎】效果的次数'
    ,th_first_trade_date                     STRING COMMENT '第一次在交易行进行交易日期'
    ,th_total_prchs_times                    BIGINT COMMENT '交易行累计购买次数'
    ,th_total_sales_times                    BIGINT COMMENT '交易行累计卖出次数'
    ,th_flame_elementium_aqr_amt             BIGINT COMMENT '交易行初火源质累计收入'
    ,th_flame_elementium_cnsum_amt           BIGINT COMMENT '交易行初火源质累计支出'
    ,th_flame_elementium_aqr_max_amt         BIGINT COMMENT '交易行初火源质单笔最大收入'
    ,th_flame_elementium_cnsum_max_amt       BIGINT COMMENT '交易行初火源质单笔最大支出'
    ,total_dead_times                        BIGINT COMMENT '总死亡次数'
    ,appearance_amt                          BIGINT COMMENT '外观获取数量'
    ,pactspirit_amt                          BIGINT COMMENT '契灵获取数量'
    ,in_hideout_mins                         BIGINT COMMENT '主城停留时间'
    ,cube_open_times                         BIGINT COMMENT '魔方开启次数'
    ,greed_times                             BIGINT COMMENT '选择「贪婪」的次数'
    ,greed_success_times                     BIGINT COMMENT '成功「贪婪」的次数 '
    ,divinity_count                          BIGINT COMMENT '神格石板收集数量'
    ,tower_complete_count                    BIGINT COMMENT '通关层数'
    ,tower_total_kill_num                    BIGINT COMMENT '怪物击杀数量'
    ,role_name_season_max_level              STRING COMMENT '赛季最高等级对应的角色名'
    ,max_flame_income_ins4gameplay           BIGINT COMMENT '单次通过永恒迷城获得最多初火源质数量'
    ,all_flame_income_ins4gameplay           BIGINT COMMENT '通过永恒迷城累计获得初火源质数量'
    ,forever_income_ins4gameplay             BIGINT COMMENT '永恒残页获得数量'
    ,cand_income_ins4gameplay                BIGINT COMMENT '魂烛历史获得数量'
    ,orange_times                            BIGINT COMMENT '传奇奖励获得次数'
    ,mutated_times                           BIGINT COMMENT '魂烛合成畸变的数量'
    ,infinite_difficulty_upper_limit         BIGINT COMMENT '无限永恒迷城最高层数'
    ,totl_killed_amt_rank                    BIGINT COMMENT '累计怪物击杀数量排名'
    ,dungeon_complete_times_percentage       BIGINT COMMENT 'REMAIN'
    ,totl_killed_amt_percentage              DOUBLE COMMENT '累计怪物击杀数量排名百分比'
    ,red_times                               BIGINT COMMENT '至臻奖励获得次数'
    ,dream_enter_times                       BIGINT COMMENT '美梦开启次数'
    ,nightmare_enter_times                   BIGINT COMMENT '进入噩梦次数'
    ,nightmare_dead_times                    BIGINT COMMENT '在噩梦中死亡次数'
    ,bub_count                               BIGINT COMMENT '泡影获得数量（噩梦成功开启的数量）'
    ,clr_bub_count                           BIGINT COMMENT '彩色泡影获得数量（噩梦成功开启的数量）'
    ,bub_lost_count                          BIGINT COMMENT '失去的泡影数量（噩梦）'
    ,clr_bub_lost_count                      BIGINT COMMENT '失去彩色泡泡数量（噩梦）'
    ,nightmare_sum_flam                      BIGINT COMMENT '在噩梦中获得的初火源质数量'
    ,nightmare_max_flam                      BIGINT COMMENT '单次噩梦获得最多初火源质数量'
    ,per_max_flame_consume                   BIGINT COMMENT '单件装备打造最多消耗火量'
    ,upgrade_lost_num                        BIGINT COMMENT '累计升阶消失稀有词缀数量'
    ,account_totl_killed_amt_rank            BIGINT COMMENT '生涯累计怪物击杀数量排名'
    ,account_totl_killed_amt_percentage      DOUBLE COMMENT '生涯累计怪物击杀数量排名百分比'
    ,max_pass_s6_times                       BIGINT COMMENT '最高连续通关雾都次数'
    ,item_990003_income_amount               BIGINT COMMENT '感染进度累计获得数量'
    ,item_990004_income_amount               BIGINT COMMENT '推理记录累计获得数量'
    ,min_15days_sanity                       BIGINT COMMENT '存活15天时最少理智消耗'
    ,max_15days_sanity                       BIGINT COMMENT '存活15天时最多理智消耗'
    ,totl_alive_days                         BIGINT COMMENT '累计存活天数'
    ,red_skill_income_amount                 BIGINT COMMENT '至臻触媒技能获得数量'
    ,fight_laker_times                       BIGINT COMMENT '雾都孤女遇见次数'
    ,most_eaten_food                         STRING COMMENT '食用次数最多的食物'
    ,most_hold_thing                         STRING COMMENT '持有天数最多的旧物'
    ,totl_pass_times                         BIGINT COMMENT '累计通关雾都次数'
    ,role_id_season_max_level                STRING COMMENT '赛季最高等级对应的角色ID'
    ,s7_open_amount                          BIGINT COMMENT '一共开启了多少次俱乐部游戏'
    ,s7_gear_amount                          BIGINT COMMENT '赛季累计获得齿轮数量'
    ,s7_clrgear_amount                       BIGINT COMMENT '彩色齿轮获得数量'
    ,s7_max_gear_once_amount                 BIGINT COMMENT '单局最多获得的齿轮数量'
    ,s7_max_clrgear_once_amount              BIGINT COMMENT '单局最多获得的彩色齿轮数量'
    ,s7_boss_battle_amount                   BIGINT COMMENT '赛季BOSS挑战次数'
    ,s7_spcl_event_amount                    BIGINT COMMENT '特殊事件触发次数（彩色）'
    ,s7_president_amount                     BIGINT COMMENT '玩偶嘉年华触发次数'
    ,s8_draw_done_amount                     BIGINT COMMENT '总计完成绘画多少次'
    ,s8_max_7block_amount                    BIGINT COMMENT '单局最多绘制几个7级地块'
    ,s8_max_7box_amount                      BIGINT COMMENT '单局最多开启绘制几个7级宝箱'
    ,s8_sum_7egg_amount                      BIGINT COMMENT '累计开启7级异彩之卵数量'
    ,s8_sum_askill_amount                    BIGINT COMMENT '累计获得华贵辅助技能数量'
    ,s8_sum_sskill_amount                    BIGINT COMMENT '累计获得崇高辅助技能数量'
    ,s8_max_flame_amount                     BIGINT COMMENT '单局最多获得初火源质数量'
    ,s8_sum_flame_amount                     BIGINT COMMENT '累计获得初火源质数量'
    ,s8_sum_destory_amount                   BIGINT COMMENT '使用强制调色功能摧毁地块总数量'
    ,s8_max_7block_amount_percentage         DOUBLE COMMENT '单局最多绘制7级地块排名百分比'
    ,s8_max_7box_amount_percentage           DOUBLE COMMENT '单局最多绘制7级宝箱排名百分比'
    ,summit_open_times                       BIGINT COMMENT '本赛季巅峰对决挑战总次数'
    ,summit_success_max_layer                BIGINT COMMENT '本赛季巅峰对决成功挑战的最高层数'
    ,summit_max_retry_layer                  BIGINT COMMENT '本赛季巅峰对决重试次数最多的层数'
    ,summit_max_retry_times                  BIGINT COMMENT '本赛季巅峰对决单层最多重试次数'
    ,s9_tarot_amount                         BIGINT COMMENT '总计收集塔罗牌数量'
    ,s9_tarot_enter_amount                   BIGINT COMMENT '总计进入塔罗秘径次数'
    ,s9_tarot_dead_amount                    BIGINT COMMENT '总计塔罗秘径内被击败次数'
    ,s9_dead_skill_percentage                BIGINT COMMENT 'REMAIN'
    ,s9_dead_skill_amount                    BIGINT COMMENT '致死最多的技能致死次数'
    ,s9_clr_case_once_amount                 BIGINT COMMENT '单局彩色宝箱最高开启个数'
    ,s9_clr_case_amount                      BIGINT COMMENT '彩色宝箱累计开启数量'
    ,s9_tianming_amount                      BIGINT COMMENT '累计获得天命数量'
    ,s9_forge_upgrade_times                  BIGINT COMMENT '总计装备升阶次数'
    ,s9_forge_upgrade_success_times          BIGINT COMMENT '总计装备升阶成功次数'
    ,s9_forge_max_fail_times                 BIGINT COMMENT '装备连续升阶失败次数'
    ,s9_forge_success_rate                   DOUBLE COMMENT '装备升阶成功率'
    ,s9_forge_success_rate_rank              DOUBLE COMMENT '装备升阶成功率排行'
    ,s9_dead_skill                           STRING COMMENT '致死最多的技能'
    ,s10_pals_amount                         BIGINT COMMENT '累计招募劳工数量'
    ,s10_trade_amount                        BIGINT COMMENT '累计进行贸易次数'
    ,s10_pillage_amount                      BIGINT COMMENT '累计进行劫掠次数'
    ,s10_carry_resus                         BIGINT COMMENT '单次贸易最高携带资源量'
    ,s10_max_flame_amount                    BIGINT COMMENT '单次贸易获得最多初火源质数'
    ,s10_spices_amount                       BIGINT COMMENT '累计带回香料数量'
    ,s10_10spices_amount                     BIGINT COMMENT '累计带回10级香料数量'
    ,s10_totl_coins_acq                      BIGINT COMMENT '空岛金币总获得量'
    ,s10_totl_invest                         BIGINT COMMENT '绿洲总注资'
    ,s_lable                                 STRING COMMENT '赛季标签'
)
PARTITIONED BY
(
    dt                                       STRING COMMENT '业务日期,yyyy-mm-dd'
)
STORED AS ALIORC
;



-- ALTER TABLE tapdb_one_data.dm_torchlight_account_career_df
-- ADD COLUMNS (
--         --  s10_pals_amount      BIGINT COMMENT '累计招募劳工数量'
--         -- ,s10_trade_amount     BIGINT COMMENT '累计进行贸易次数'
--         -- ,s10_pillage_amount   BIGINT COMMENT '累计进行劫掠次数'
--         -- ,s10_carry_resus      BIGINT COMMENT '单次贸易最高携带资源量'
--         -- ,s10_max_flame_amount BIGINT COMMENT '单次贸易获得最多初火源质数'
--         -- ,s10_spices_amount    BIGINT COMMENT '累计带回香料数量'
--         -- ,s10_10spices_amount  BIGINT COMMENT '累计带回10级香料数量'
--         -- ,s10_totl_coins_acq   BIGINT COMMENT '空岛金币总获得量'
--         -- ,s10_totl_invest      BIGINT COMMENT '绿洲总注资'

--         --  hijack_car_cnt                        BIGINT COMMENT '累计劫车次数'
--         -- ,bounty_complete_cnt                   BIGINT COMMENT '累计完成悬赏订单次数'
--         -- ,premium_bounty_complete_cnt           BIGINT COMMENT '累计完成天价订单次数'
--         -- ,deep_research_success_cnt             BIGINT COMMENT '深度研发成功次数'
--         -- ,runaway_monster_kill_cnt              BIGINT COMMENT '累计击杀逃跑怪数量'
--         -- ,lucky_moment_success_cnt              BIGINT COMMENT '好运时刻成功次数'
--         -- ,tower_coin_gain_sum                   BIGINT COMMENT '累计获得高塔币数量'
--         -- ,central_vault_small_chest_plunder_cnt BIGINT COMMENT '高塔中央金库小保险箱劫掠数量'
--         -- ,central_vault_large_chest_open_cnt    BIGINT COMMENT '高塔中央金库大保险箱开启次数'

--         total_pass_gate_count        BIGINT COMMENT '累计通过叠界门次数'
--         ,total_enter_layer4_count    BIGINT COMMENT '累计进入叠界第4层次数'
--         ,total_kill_gatekeeper_count BIGINT COMMENT '累计击杀守门人次数'
--         ,total_kill_hunter_count     BIGINT COMMENT '累计击杀狩门人次数'
--         ,total_colored_bottle_count  BIGINT COMMENT '累计获得彩色瓶中叠影数量'
--         ,total_nixiang_count         BIGINT COMMENT '累计掉落逆像数量'
--         ,total_disturbance_count     BIGINT COMMENT '累计遭遇叠界扰动次数'
--         ,total_pickup_skull_count    BIGINT COMMENT '累计捡起漂浮头颅数量'
-- );

-- ALTER TABLE tapdb_one_data.dm_torchlight_account_career_df
-- ADD COLUMNS (
--         -- S13 终局玩法指标
--         s13_craving_substance_cnt    BIGINT COMMENT '累计获得渴瘾物质数量 (coin_id=826)'
--         ,s13_perfect_organ_cnt       BIGINT COMMENT '累计掉落完美器官数量'
--         ,s13_scavenger_kill_cnt      BIGINT COMMENT '累计击杀清道夫数量'
--         ,s13_level_open_cnt          BIGINT COMMENT '终局玩法开启总次数'
--         ,s13_level_score_max         BIGINT COMMENT '终局玩法单局最高分'
--         ,s13_level_score_min         BIGINT COMMENT '终局玩法单局最低分'
--         ,s13_colored_jar_cnt         BIGINT COMMENT '累积开启彩色罐子数'
--         ,s13_max_monster_num         BIGINT COMMENT '终局玩法单局养成怪物最多数量'
--         ,s13_max_single_monster_score BIGINT COMMENT '终局玩法养成最高单个怪物分'
--         ,s13_most_used_modifier      BIGINT COMMENT '选择次数最多的手术用具(遗物牌)'
--         ,s13_most_used_effect        BIGINT COMMENT '选择次数最多的药剂(效果牌)'
--         ,s13_total_vitality          BIGINT COMMENT '赛季内累计获得的总活性'
-- );



INSERT OVERWRITE TABLE tapdb_one_data.dm_torchlight_account_career_df PARTITION (dt = '${dt}')
SELECT  all.account
        ,all.season
        ,all.totl_login_days
        ,all.totl_play_sec
        ,all.sesn_login_days
        ,all.sesn_play_sec
        ,all.totl_killed_amt
        ,all.highest_hero_purchase_level
        ,all.dungeon_complete_times
        ,all.dungeon_plane_watcher_killed_times
        ,all.dungeon_realm_lord_killed_times
        ,all.dungeon_keegan_and_pirates_killed_times
        ,all.gow_open_times
        ,all.gop_open_times
        ,all.goh_open_times
        ,all.gom_open_times
        ,all.flame_elementium_aqr_amt
        ,all.flame_sand_aqr_amt
        ,all.flame_dust_aqr_amt
        ,all.ember_aqr_amt
        ,all.flame_elementium_craft_cnsum_amt
        ,all.flame_sand_craft_cnsum_amt
        ,all.flame_dust_craft_cnsum_amt
        ,all.ember_craft_cnsum_amt
        ,all.flame_elementium_aqr_maximum_day_amt
        ,fluor.fluorescent_memory_aqr_amt
        ,all.compass_aqr_amt
        ,all.legendary_gear_aqr_amt
        ,all.other_gear_aqr_amt
        ,all.alevel_legendary_gear_aqr_amt
        ,all.blevel_legendary_gear_aqr_amt
        ,all.gear_corroded_times
        ,all.gear_defiled_times
        ,all.th_first_trade_date
        ,all.th_total_prchs_times
        ,all.th_total_sales_times
        ,all.th_flame_elementium_aqr_amt
        ,all.th_flame_elementium_cnsum_amt
        ,all.th_flame_elementium_aqr_max_amt
        ,all.th_flame_elementium_cnsum_max_amt
        ,all.total_dead_times
        ,all.appearance_amt
        ,all.pactspirit_amt
        ,all.in_hideout_mins
        ,all.cube_open_times
        ,all.greed_times
        ,all.greed_success_times
        ,all.divinity_count
        ,all.tower_complete_count
        ,all.tower_total_kill_num
        ,all.role_name_season_max_level
        ,all.max_flame_income_ins4gameplay
        ,all.all_flame_income_ins4gameplay
        ,all.forever_income_ins4gameplay
        ,all.cand_income_ins4gameplay
        ,all.orange_times
        ,all.mutated_times
        ,all.infinite_difficulty_upper_limit
        ,all.totl_killed_amt_rank
        ,all.dungeon_complete_times_percentage
        ,all.totl_killed_amt_percentage
        ,all.red_times
        ,all.dream_enter_times
        ,all.nightmare_enter_times
        ,all.nightmare_dead_times
        ,all.bub_count
        ,all.clr_bub_count
        ,all.bub_lost_count
        ,all.clr_bub_lost_count
        ,all.nightmare_sum_flam
        ,all.nightmare_max_flam
        ,all.per_max_flame_consume
        ,all.upgrade_lost_num
        ,all.account_totl_killed_amt_rank
        ,all.account_totl_killed_amt_percentage
        ,all.max_pass_s6_times
        ,all.item_990003_income_amount
        ,all.item_990004_income_amount
        ,all.min_15days_sanity
        ,all.max_15days_sanity
        ,all.totl_alive_days
        ,all.red_skill_income_amount
        ,all.fight_laker_times
        ,all.most_eaten_food
        ,all.most_hold_thing
        ,all.totl_pass_times
        ,all.role_id_season_max_level
        ,all.s7_open_amount
        ,all.s7_gear_amount
        ,all.s7_clrgear_amount
        ,all.s7_max_gear_once_amount
        ,all.s7_max_clrgear_once_amount
        ,all.s7_boss_battle_amount
        ,all.s7_spcl_event_amount
        ,all.s7_president_amount
        ,all.s8_draw_done_amount
        ,all.s8_max_7block_amount
        ,all.s8_max_7box_amount
        ,all.s8_sum_7egg_amount
        ,all.s8_sum_askill_amount
        ,all.s8_sum_sskill_amount
        ,all.s8_max_flame_amount
        ,all.s8_sum_flame_amount
        ,all.s8_sum_destory_amount
        ,all.s8_max_7block_amount_percentage
        ,all.s8_max_7box_amount_percentage
        ,all.summit_open_times
        ,all.summit_success_max_layer
        ,all.summit_max_retry_layer
        ,all.summit_max_retry_times
        ,all.s9_tarot_amount
        ,all.s9_tarot_enter_amount
        ,all.s9_tarot_dead_amount
        ,all.s9_dead_skill_percentage
        ,all.s9_dead_skill_amount
        ,all.s9_clr_case_once_amount
        ,all.s9_clr_case_amount
        ,all.s9_tianming_amount
        ,all.s9_forge_upgrade_times
        ,all.s9_forge_upgrade_success_times
        ,all.s9_forge_max_fail_times
        ,all.s9_forge_success_rate
        ,all.s9_forge_success_rate_rank
        ,all.s9_dead_skill
        ,all.s10_pals_amount
        ,all.s10_trade_amount
        ,all.s10_pillage_amount
        ,all.s10_carry_resus
        ,all.s10_max_flame_amount
        ,all.s10_spices_amount
        ,all.s10_10spices_amount
        ,all.s10_totl_coins_acq
        ,all.s10_totl_invest
        ,all.s_label

        ,all.hijack_car_cnt
        ,all.bounty_complete_cnt
        ,all.premium_bounty_complete_cnt
        ,all.deep_research_success_cnt
        ,all.runaway_monster_kill_cnt
        ,all.lucky_moment_success_cnt
        ,all.tower_coin_gain_sum
        ,all.central_vault_small_chest_plunder_cnt
        ,all.central_vault_large_chest_open_cnt

        ,all.total_pass_gate_count
        ,all.total_enter_layer4_count
        ,all.total_kill_gatekeeper_count
        ,all.total_kill_hunter_count
        ,all.total_colored_bottle_count
        ,all.total_nixiang_count
        ,all.total_disturbance_count
        ,all.total_pickup_skull_count

        -- S13 指标
        ,all.s13_craving_substance_cnt
        ,all.s13_perfect_organ_cnt
        ,all.s13_scavenger_kill_cnt
        ,all.s13_level_open_cnt
        ,all.s13_level_score_max
        ,all.s13_level_score_min
        ,all.s13_colored_jar_cnt
        ,all.s13_max_monster_num
        ,all.s13_max_single_monster_score
        ,all.s13_most_used_modifier
        ,all.s13_most_used_effect
        ,all.s13_total_vitality

FROM    (
-- SELECT  *
-- FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f
-- WHERE   s_label = 'S3' AND season >= 301 AND season < 401
-- AND     account = '483644537110286337'
SELECT  s3.account
        ,s3.season
        ,s3.totl_login_days,s3.totl_play_sec,s3.sesn_login_days,s3.sesn_play_sec,s3.totl_killed_amt,s3.highest_hero_purchase_level,s3.dungeon_complete_times,s3.dungeon_plane_watcher_killed_times,s3.dungeon_realm_lord_killed_times,s3.dungeon_keegan_and_pirates_killed_times,s3.gow_open_times,s3.gop_open_times,s3.goh_open_times,s3.gom_open_times,s3.flame_elementium_aqr_amt,s3.flame_sand_aqr_amt,s3.flame_dust_aqr_amt,s3.ember_aqr_amt,s3.flame_elementium_craft_cnsum_amt,s3.flame_sand_craft_cnsum_amt,s3.flame_dust_craft_cnsum_amt,s3.ember_craft_cnsum_amt,s3.flame_elementium_aqr_maximum_day_amt,s3.fluorescent_memory_aqr_amt,s3.compass_aqr_amt,s3.legendary_gear_aqr_amt,s3.other_gear_aqr_amt,s3.alevel_legendary_gear_aqr_amt,s3.blevel_legendary_gear_aqr_amt,s3.gear_corroded_times,s3.gear_defiled_times,s3.th_first_trade_date,s3.th_total_prchs_times,s3.th_total_sales_times,s3.th_flame_elementium_aqr_amt,s3.th_flame_elementium_cnsum_amt,s3.th_flame_elementium_aqr_max_amt,s3.th_flame_elementium_cnsum_max_amt,s3.total_dead_times,s3.appearance_amt,s3.pactspirit_amt,s3.in_hideout_mins,s3.cube_open_times,s3.greed_times,s3.greed_success_times,s3.divinity_count,s3.tower_complete_count,s3.tower_total_kill_num,s3.role_name_season_max_level,s3.max_flame_income_ins4gameplay,s3.all_flame_income_ins4gameplay,s3.forever_income_ins4gameplay,s3.cand_income_ins4gameplay,s3.orange_times,s3.mutated_times,s3.infinite_difficulty_upper_limit,s3.totl_killed_amt_rank,s3.dungeon_complete_times_percentage,s3.totl_killed_amt_percentage,s3.red_times,s3.dream_enter_times,s3.nightmare_enter_times,s3.nightmare_dead_times,s3.bub_count,s3.clr_bub_count,s3.bub_lost_count,s3.clr_bub_lost_count,s3.nightmare_sum_flam,s3.nightmare_max_flam,s3.per_max_flame_consume,s3.upgrade_lost_num,s3.account_totl_killed_amt_rank,s3.account_totl_killed_amt_percentage,s3.max_pass_s6_times,s3.item_990003_income_amount,s3.item_990004_income_amount,s3.min_15days_sanity,s3.max_15days_sanity,s3.totl_alive_days,s3.red_skill_income_amount,s3.fight_laker_times,s3.most_eaten_food,s3.most_hold_thing,s3.totl_pass_times
        ,COALESCE(s7.role_id_season_max_level, s3.role_id_season_max_level) AS role_id_season_max_level
        ,s3.s7_open_amount,s3.s7_gear_amount,s3.s7_clrgear_amount,s3.s7_max_gear_once_amount,s3.s7_max_clrgear_once_amount,s3.s7_boss_battle_amount,s3.s7_spcl_event_amount,s3.s7_president_amount,s3.s8_draw_done_amount,s3.s8_max_7block_amount,s3.s8_max_7box_amount,s3.s8_sum_7egg_amount,s3.s8_sum_askill_amount,s3.s8_sum_sskill_amount,s3.s8_max_flame_amount,s3.s8_sum_flame_amount,s3.s8_sum_destory_amount,s3.s8_max_7block_amount_percentage,s3.s8_max_7box_amount_percentage,s3.summit_open_times,s3.summit_success_max_layer,s3.summit_max_retry_layer,s3.summit_max_retry_times,s3.s9_tarot_amount,s3.s9_tarot_enter_amount,s3.s9_tarot_dead_amount,s3.s9_dead_skill_percentage,s3.s9_dead_skill_amount,s3.s9_clr_case_once_amount,s3.s9_clr_case_amount,s3.s9_tianming_amount,s3.s9_forge_upgrade_times,s3.s9_forge_upgrade_success_times,s3.s9_forge_max_fail_times,s3.s9_forge_success_rate,s3.s9_forge_success_rate_rank,s3.s9_dead_skill,s3.s10_pals_amount,s3.s10_trade_amount,s3.s10_pillage_amount,s3.s10_carry_resus,s3.s10_max_flame_amount,s3.s10_spices_amount,s3.s10_10spices_amount,s3.s10_totl_coins_acq,s3.s10_totl_invest
        ,s3.s_label,s3.hijack_car_cnt,s3.bounty_complete_cnt,s3.premium_bounty_complete_cnt,s3.deep_research_success_cnt,s3.runaway_monster_kill_cnt,s3.lucky_moment_success_cnt,s3.tower_coin_gain_sum,s3.central_vault_small_chest_plunder_cnt,s3.central_vault_large_chest_open_cnt,s3.total_pass_gate_count ,s3.total_enter_layer4_count ,s3.total_kill_gatekeeper_count ,s3.total_kill_hunter_count ,s3.total_colored_bottle_count ,s3.total_nixiang_count ,s3.total_disturbance_count ,s3.total_pickup_skull_count
        ,0 AS s13_craving_substance_cnt,0 AS s13_perfect_organ_cnt,0 AS s13_scavenger_kill_cnt,0 AS s13_level_open_cnt,0 AS s13_level_score_max,0 AS s13_level_score_min,0 AS s13_colored_jar_cnt,0 AS s13_max_monster_num,0 AS s13_max_single_monster_score,0 AS s13_most_used_modifier,0 AS s13_most_used_effect,0 AS s13_total_vitality
FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f s3
LEFT JOIN tapdb_one_data.dws_torchlight_account_career_his_all_f s7
       ON s7.account = s3.account
      AND s7.season  = s3.season
      AND s7.s_label = 'S7'
WHERE   s3.s_label = 'S3'
AND   s3.season >= 301 AND s3.season < 401


UNION ALL
-- SELECT  *
-- FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f
-- WHERE   s_label = 'S4' AND season >= 401 AND season < 501

SELECT  s3.account
        ,s3.season
        ,s3.totl_login_days,s3.totl_play_sec,s3.sesn_login_days,s3.sesn_play_sec,s3.totl_killed_amt,s3.highest_hero_purchase_level,s3.dungeon_complete_times,s3.dungeon_plane_watcher_killed_times,s3.dungeon_realm_lord_killed_times,s3.dungeon_keegan_and_pirates_killed_times,s3.gow_open_times,s3.gop_open_times,s3.goh_open_times,s3.gom_open_times,s3.flame_elementium_aqr_amt,s3.flame_sand_aqr_amt,s3.flame_dust_aqr_amt,s3.ember_aqr_amt,s3.flame_elementium_craft_cnsum_amt,s3.flame_sand_craft_cnsum_amt,s3.flame_dust_craft_cnsum_amt,s3.ember_craft_cnsum_amt,s3.flame_elementium_aqr_maximum_day_amt,s3.fluorescent_memory_aqr_amt,s3.compass_aqr_amt,s3.legendary_gear_aqr_amt,s3.other_gear_aqr_amt,s3.alevel_legendary_gear_aqr_amt,s3.blevel_legendary_gear_aqr_amt,s3.gear_corroded_times,s3.gear_defiled_times,s3.th_first_trade_date,s3.th_total_prchs_times,s3.th_total_sales_times,s3.th_flame_elementium_aqr_amt,s3.th_flame_elementium_cnsum_amt,s3.th_flame_elementium_aqr_max_amt,s3.th_flame_elementium_cnsum_max_amt,s3.total_dead_times,s3.appearance_amt,s3.pactspirit_amt,s3.in_hideout_mins,s3.cube_open_times,s3.greed_times,s3.greed_success_times,s3.divinity_count,s3.tower_complete_count,s3.tower_total_kill_num,s3.role_name_season_max_level,s3.max_flame_income_ins4gameplay,s3.all_flame_income_ins4gameplay,s3.forever_income_ins4gameplay,s3.cand_income_ins4gameplay,s3.orange_times,s3.mutated_times,s3.infinite_difficulty_upper_limit,s3.totl_killed_amt_rank,s3.dungeon_complete_times_percentage,s3.totl_killed_amt_percentage,s3.red_times,s3.dream_enter_times,s3.nightmare_enter_times,s3.nightmare_dead_times,s3.bub_count,s3.clr_bub_count,s3.bub_lost_count,s3.clr_bub_lost_count,s3.nightmare_sum_flam,s3.nightmare_max_flam,s3.per_max_flame_consume,s3.upgrade_lost_num,s3.account_totl_killed_amt_rank,s3.account_totl_killed_amt_percentage,s3.max_pass_s6_times,s3.item_990003_income_amount,s3.item_990004_income_amount,s3.min_15days_sanity,s3.max_15days_sanity,s3.totl_alive_days,s3.red_skill_income_amount,s3.fight_laker_times,s3.most_eaten_food,s3.most_hold_thing,s3.totl_pass_times
        ,COALESCE(s7.role_id_season_max_level, s3.role_id_season_max_level) AS role_id_season_max_level
        ,s3.s7_open_amount,s3.s7_gear_amount,s3.s7_clrgear_amount,s3.s7_max_gear_once_amount,s3.s7_max_clrgear_once_amount,s3.s7_boss_battle_amount,s3.s7_spcl_event_amount,s3.s7_president_amount,s3.s8_draw_done_amount,s3.s8_max_7block_amount,s3.s8_max_7box_amount,s3.s8_sum_7egg_amount,s3.s8_sum_askill_amount,s3.s8_sum_sskill_amount,s3.s8_max_flame_amount,s3.s8_sum_flame_amount,s3.s8_sum_destory_amount,s3.s8_max_7block_amount_percentage,s3.s8_max_7box_amount_percentage,s3.summit_open_times,s3.summit_success_max_layer,s3.summit_max_retry_layer,s3.summit_max_retry_times,s3.s9_tarot_amount,s3.s9_tarot_enter_amount,s3.s9_tarot_dead_amount,s3.s9_dead_skill_percentage,s3.s9_dead_skill_amount,s3.s9_clr_case_once_amount,s3.s9_clr_case_amount,s3.s9_tianming_amount,s3.s9_forge_upgrade_times,s3.s9_forge_upgrade_success_times,s3.s9_forge_max_fail_times,s3.s9_forge_success_rate,s3.s9_forge_success_rate_rank,s3.s9_dead_skill,s3.s10_pals_amount,s3.s10_trade_amount,s3.s10_pillage_amount,s3.s10_carry_resus,s3.s10_max_flame_amount,s3.s10_spices_amount,s3.s10_10spices_amount,s3.s10_totl_coins_acq,s3.s10_totl_invest
        ,s3.s_label,s3.hijack_car_cnt,s3.bounty_complete_cnt,s3.premium_bounty_complete_cnt,s3.deep_research_success_cnt,s3.runaway_monster_kill_cnt,s3.lucky_moment_success_cnt,s3.tower_coin_gain_sum,s3.central_vault_small_chest_plunder_cnt,s3.central_vault_large_chest_open_cnt,s3.total_pass_gate_count ,s3.total_enter_layer4_count ,s3.total_kill_gatekeeper_count ,s3.total_kill_hunter_count ,s3.total_colored_bottle_count ,s3.total_nixiang_count ,s3.total_disturbance_count ,s3.total_pickup_skull_count
        ,0 AS s13_craving_substance_cnt,0 AS s13_perfect_organ_cnt,0 AS s13_scavenger_kill_cnt,0 AS s13_level_open_cnt,0 AS s13_level_score_max,0 AS s13_level_score_min,0 AS s13_colored_jar_cnt,0 AS s13_max_monster_num,0 AS s13_max_single_monster_score,0 AS s13_most_used_modifier,0 AS s13_most_used_effect,0 AS s13_total_vitality
FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f s3
LEFT JOIN tapdb_one_data.dws_torchlight_account_career_his_all_f s7
       ON s7.account = s3.account
      AND s7.season  = s3.season
      AND s7.s_label = 'S7'
WHERE   s3.s_label = 'S4'
AND   s3.season >= 401 AND s3.season < 501

UNION ALL
-- SELECT  *
-- FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f
-- WHERE   s_label = 'S5' AND season >= 501 AND season < 601

SELECT  s3.account
        ,s3.season
        ,s3.totl_login_days,s3.totl_play_sec,s3.sesn_login_days,s3.sesn_play_sec,s3.totl_killed_amt,s3.highest_hero_purchase_level,s3.dungeon_complete_times,s3.dungeon_plane_watcher_killed_times,s3.dungeon_realm_lord_killed_times,s3.dungeon_keegan_and_pirates_killed_times,s3.gow_open_times,s3.gop_open_times,s3.goh_open_times,s3.gom_open_times,s3.flame_elementium_aqr_amt,s3.flame_sand_aqr_amt,s3.flame_dust_aqr_amt,s3.ember_aqr_amt,s3.flame_elementium_craft_cnsum_amt,s3.flame_sand_craft_cnsum_amt,s3.flame_dust_craft_cnsum_amt,s3.ember_craft_cnsum_amt,s3.flame_elementium_aqr_maximum_day_amt,s3.fluorescent_memory_aqr_amt,s3.compass_aqr_amt,s3.legendary_gear_aqr_amt,s3.other_gear_aqr_amt,s3.alevel_legendary_gear_aqr_amt,s3.blevel_legendary_gear_aqr_amt,s3.gear_corroded_times,s3.gear_defiled_times,s3.th_first_trade_date,s3.th_total_prchs_times,s3.th_total_sales_times,s3.th_flame_elementium_aqr_amt,s3.th_flame_elementium_cnsum_amt,s3.th_flame_elementium_aqr_max_amt,s3.th_flame_elementium_cnsum_max_amt,s3.total_dead_times,s3.appearance_amt,s3.pactspirit_amt,s3.in_hideout_mins,s3.cube_open_times,s3.greed_times,s3.greed_success_times,s3.divinity_count,s3.tower_complete_count,s3.tower_total_kill_num,s3.role_name_season_max_level,s3.max_flame_income_ins4gameplay,s3.all_flame_income_ins4gameplay,s3.forever_income_ins4gameplay,s3.cand_income_ins4gameplay,s3.orange_times,s3.mutated_times,s3.infinite_difficulty_upper_limit,s3.totl_killed_amt_rank,s3.dungeon_complete_times_percentage,s3.totl_killed_amt_percentage,s3.red_times,s3.dream_enter_times,s3.nightmare_enter_times,s3.nightmare_dead_times,s3.bub_count,s3.clr_bub_count,s3.bub_lost_count,s3.clr_bub_lost_count,s3.nightmare_sum_flam,s3.nightmare_max_flam,s3.per_max_flame_consume,s3.upgrade_lost_num,s3.account_totl_killed_amt_rank,s3.account_totl_killed_amt_percentage,s3.max_pass_s6_times,s3.item_990003_income_amount,s3.item_990004_income_amount,s3.min_15days_sanity,s3.max_15days_sanity,s3.totl_alive_days,s3.red_skill_income_amount,s3.fight_laker_times,s3.most_eaten_food,s3.most_hold_thing,s3.totl_pass_times
        ,COALESCE(s7.role_id_season_max_level, s3.role_id_season_max_level) AS role_id_season_max_level
        ,s3.s7_open_amount,s3.s7_gear_amount,s3.s7_clrgear_amount,s3.s7_max_gear_once_amount,s3.s7_max_clrgear_once_amount,s3.s7_boss_battle_amount,s3.s7_spcl_event_amount,s3.s7_president_amount,s3.s8_draw_done_amount,s3.s8_max_7block_amount,s3.s8_max_7box_amount,s3.s8_sum_7egg_amount,s3.s8_sum_askill_amount,s3.s8_sum_sskill_amount,s3.s8_max_flame_amount,s3.s8_sum_flame_amount,s3.s8_sum_destory_amount,s3.s8_max_7block_amount_percentage,s3.s8_max_7box_amount_percentage,s3.summit_open_times,s3.summit_success_max_layer,s3.summit_max_retry_layer,s3.summit_max_retry_times,s3.s9_tarot_amount,s3.s9_tarot_enter_amount,s3.s9_tarot_dead_amount,s3.s9_dead_skill_percentage,s3.s9_dead_skill_amount,s3.s9_clr_case_once_amount,s3.s9_clr_case_amount,s3.s9_tianming_amount,s3.s9_forge_upgrade_times,s3.s9_forge_upgrade_success_times,s3.s9_forge_max_fail_times,s3.s9_forge_success_rate,s3.s9_forge_success_rate_rank,s3.s9_dead_skill,s3.s10_pals_amount,s3.s10_trade_amount,s3.s10_pillage_amount,s3.s10_carry_resus,s3.s10_max_flame_amount,s3.s10_spices_amount,s3.s10_10spices_amount,s3.s10_totl_coins_acq,s3.s10_totl_invest
        ,s3.s_label,s3.hijack_car_cnt,s3.bounty_complete_cnt,s3.premium_bounty_complete_cnt,s3.deep_research_success_cnt,s3.runaway_monster_kill_cnt,s3.lucky_moment_success_cnt,s3.tower_coin_gain_sum,s3.central_vault_small_chest_plunder_cnt,s3.central_vault_large_chest_open_cnt,s3.total_pass_gate_count ,s3.total_enter_layer4_count ,s3.total_kill_gatekeeper_count ,s3.total_kill_hunter_count ,s3.total_colored_bottle_count ,s3.total_nixiang_count ,s3.total_disturbance_count ,s3.total_pickup_skull_count
        ,0 AS s13_craving_substance_cnt,0 AS s13_perfect_organ_cnt,0 AS s13_scavenger_kill_cnt,0 AS s13_level_open_cnt,0 AS s13_level_score_max,0 AS s13_level_score_min,0 AS s13_colored_jar_cnt,0 AS s13_max_monster_num,0 AS s13_max_single_monster_score,0 AS s13_most_used_modifier,0 AS s13_most_used_effect,0 AS s13_total_vitality
FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f s3
LEFT JOIN tapdb_one_data.dws_torchlight_account_career_his_all_f s7
       ON s7.account = s3.account
      AND s7.season  = s3.season
      AND s7.s_label = 'S7'
WHERE   s3.s_label = 'S5'
AND   s3.season >= 501 AND s3.season < 601

UNION ALL
SELECT  *
        ,0 AS s13_craving_substance_cnt,0 AS s13_perfect_organ_cnt,0 AS s13_scavenger_kill_cnt,0 AS s13_level_open_cnt,0 AS s13_level_score_max,0 AS s13_level_score_min,0 AS s13_colored_jar_cnt,0 AS s13_max_monster_num,0 AS s13_max_single_monster_score,0 AS s13_most_used_modifier,0 AS s13_most_used_effect,0 AS s13_total_vitality
FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f
WHERE   s_label = 'S6' AND season >= 601 AND season < 701
UNION ALL
SELECT  *
        ,0 AS s13_craving_substance_cnt,0 AS s13_perfect_organ_cnt,0 AS s13_scavenger_kill_cnt,0 AS s13_level_open_cnt,0 AS s13_level_score_max,0 AS s13_level_score_min,0 AS s13_colored_jar_cnt,0 AS s13_max_monster_num,0 AS s13_max_single_monster_score,0 AS s13_most_used_modifier,0 AS s13_most_used_effect,0 AS s13_total_vitality
FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f
WHERE   s_label = 'S7' AND season >= 701 AND season < 801
UNION ALL
SELECT  *
        ,0 AS s13_craving_substance_cnt,0 AS s13_perfect_organ_cnt,0 AS s13_scavenger_kill_cnt,0 AS s13_level_open_cnt,0 AS s13_level_score_max,0 AS s13_level_score_min,0 AS s13_colored_jar_cnt,0 AS s13_max_monster_num,0 AS s13_max_single_monster_score,0 AS s13_most_used_modifier,0 AS s13_most_used_effect,0 AS s13_total_vitality
FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f
WHERE   s_label = 'S8' AND season >= 801 AND season < 901
UNION ALL
SELECT  *
        ,0 AS s13_craving_substance_cnt,0 AS s13_perfect_organ_cnt,0 AS s13_scavenger_kill_cnt,0 AS s13_level_open_cnt,0 AS s13_level_score_max,0 AS s13_level_score_min,0 AS s13_colored_jar_cnt,0 AS s13_max_monster_num,0 AS s13_max_single_monster_score,0 AS s13_most_used_modifier,0 AS s13_most_used_effect,0 AS s13_total_vitality
FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f
WHERE   s_label = 'S9' AND season >= 901 AND season < 1001
UNION ALL
SELECT  *
        ,0 AS s13_craving_substance_cnt,0 AS s13_perfect_organ_cnt,0 AS s13_scavenger_kill_cnt,0 AS s13_level_open_cnt,0 AS s13_level_score_max,0 AS s13_level_score_min,0 AS s13_colored_jar_cnt,0 AS s13_max_monster_num,0 AS s13_max_single_monster_score,0 AS s13_most_used_modifier,0 AS s13_most_used_effect,0 AS s13_total_vitality
FROM    tapdb_one_data.dws_torchlight_account_career_his_all_f
WHERE   s_label = 'S10' AND season >= 1001 AND season < 1101
UNION ALL
SELECT
account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,CASE
            WHEN season >= 1301 THEN 'S13'
            WHEN season >= 1201 THEN 'S12'
            ELSE 'S11'
         END AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
        -- S13 指标：season >= 1301 时有值，S11/S12 赛季自然为 0
        ,NVL(s13_craving_substance_cnt,    0) AS s13_craving_substance_cnt
        ,NVL(s13_perfect_organ_cnt,        0) AS s13_perfect_organ_cnt
        ,NVL(s13_scavenger_kill_cnt,       0) AS s13_scavenger_kill_cnt
        ,NVL(s13_level_open_cnt,           0) AS s13_level_open_cnt
        ,NVL(s13_level_score_max,          0) AS s13_level_score_max
        ,NVL(s13_level_score_min,          0) AS s13_level_score_min
        ,NVL(s13_colored_jar_cnt,          0) AS s13_colored_jar_cnt
        ,NVL(s13_max_monster_num,          0) AS s13_max_monster_num
        ,NVL(s13_max_single_monster_score, 0) AS s13_max_single_monster_score
        ,NVL(s13_most_used_modifier,       0) AS s13_most_used_modifier
        ,NVL(s13_most_used_effect,         0) AS s13_most_used_effect
        ,NVL(s13_total_vitality,           0) AS s13_total_vitality
FROM tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '${dt}' AND season >= 1101
) all
LEFT JOIN (
        SELECT account,season,fluorescent_memory_aqr_amt FROM tapdb_one_data.dws_torchlight_account_career_his_all_f
        WHERE  s_label = 'S9' AND season < 1001
        UNION ALL
        SELECT  account,season,fluorescent_memory_aqr_amt FROM tapdb_one_data.dws_torchlight_account_career_df
        WHERE   dt = '${dt}' AND season >= 1001
) fluor
ON      all.account = fluor.account
AND     all.season = fluor.season

-- WHERE all.account = '370881762181795841'

-- )
;
