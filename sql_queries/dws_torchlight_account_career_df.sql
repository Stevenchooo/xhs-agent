--odps sql
--********************************************************************--
--author:蔡圣哲
--create time:2023-06-05 16:47:00
--********************************************************************--
USE tapdb_one_data
;

-- ALTER TABLE tapdb_one_data.dws_torchlight_account_career_df
-- ADD COLUMNS (
--         total_pass_gate_count        BIGINT COMMENT '累计通过叠界门次数'
--         ,total_enter_layer4_count    BIGINT COMMENT '累计进入叠界第4层次数'
--         ,total_kill_gatekeeper_count BIGINT COMMENT '累计击杀守门人次数'
--         ,total_kill_hunter_count     BIGINT COMMENT '累计击杀狩门人次数'
--         ,total_colored_bottle_count  BIGINT COMMENT '累计获得彩色瓶中叠影数量'
--         ,total_nixiang_count         BIGINT COMMENT '累计掉落逆像数量'
--         ,total_disturbance_count     BIGINT COMMENT '累计遭遇叠界扰动次数'
--         ,total_pickup_skull_count    BIGINT COMMENT '累计捡起漂浮头颅数量'
--         -- S13
--         ,s13_craving_substance_cnt    BIGINT COMMENT '累计获得渴瘾物质数量 (coin_id=826)'
--         ,s13_perfect_organ_cnt        BIGINT COMMENT '累计掉落完美器官数量'
--         ,s13_scavenger_kill_cnt       BIGINT COMMENT '累计击杀清道夫数量'
--         ,s13_level_open_cnt           BIGINT COMMENT '终局玩法开启总次数'
--         ,s13_level_score_max          BIGINT COMMENT '终局玩法单局最高分'
--         ,s13_level_score_min          BIGINT COMMENT '终局玩法单局最低分'
--         ,s13_colored_jar_cnt          BIGINT COMMENT '累积开启彩色罐子数'
--         ,s13_max_monster_num          BIGINT COMMENT '终局玩法单局养成怪物最多数量'
--         ,s13_max_single_monster_score BIGINT COMMENT '终局玩法养成最高单个怪物分'
--         ,s13_most_used_modifier       BIGINT COMMENT '选择次数最多的手术用具(遗物牌)'
--         ,s13_most_used_effect         BIGINT COMMENT '选择次数最多的药剂(效果牌)'
--         ,s13_total_vitality           BIGINT COMMENT '赛季内累计获得的总活性'
-- );
SET odps.sql.hive.compatible = true
;

SET odps.stage.reducer.mem = 16384
;

INSERT OVERWRITE TABLE tapdb_one_data.dws_torchlight_account_career_df PARTITION (dt = '${dt}')
SELECT  account
        ,season
        ,totl_login_days
        ,totl_play_sec
        ,sesn_login_days
        ,sesn_play_sec
        ,totl_killed_amt
        ,highest_hero_purchase_level
        ,dungeon_complete_times
        ,dungeon_plane_watcher_killed_times
        ,dungeon_realm_lord_killed_times
        ,dungeon_keegan_and_pirates_killed_times
        ,gow_open_times
        ,gop_open_times
        ,goh_open_times
        ,gom_open_times
        ,flame_elementium_aqr_amt
        ,flame_sand_aqr_amt
        ,flame_dust_aqr_amt
        ,ember_aqr_amt
        ,flame_elementium_craft_cnsum_amt
        ,flame_sand_craft_cnsum_amt
        ,flame_dust_craft_cnsum_amt
        ,ember_craft_cnsum_amt
        ,flame_elementium_aqr_maximum_day_amt
        ,fluorescent_memory_aqr_amt
        ,compass_aqr_amt
        ,legendary_gear_aqr_amt
        ,other_gear_aqr_amt
        ,alevel_legendary_gear_aqr_amt
        ,blevel_legendary_gear_aqr_amt
        ,gear_corroded_times
        ,gear_defiled_times
        ,th_first_trade_date
        ,th_total_prchs_times
        ,th_total_sales_times
        ,th_flame_elementium_aqr_amt
        ,th_flame_elementium_cnsum_amt
        ,th_flame_elementium_aqr_max_amt
        ,th_flame_elementium_cnsum_max_amt
        ,total_dead_times
        ,appearance_amt
        ,pactspirit_amt
        ,in_hideout_mins
        ,cube_open_times
        ,greed_times
        ,greed_success_times
        ,divinity_count
        ,tower_complete_count
        ,tower_total_kill_num
        ,role_name_season_max_level
        ,max_flame_income_ins4gameplay
        ,all_flame_income_ins4gameplay
        ,forever_income_ins4gameplay
        ,cand_income_ins4gameplay
        ,orange_times
        ,mutated_times
        ,infinite_difficulty_upper_limit
        ,RANK() OVER (PARTITION BY season ORDER BY totl_killed_amt DESC ) AS totl_killed_amt_rank
        ,0 AS dungeon_complete_times_percentage
        ,CAST(PERCENT_RANK() OVER (PARTITION BY season ORDER BY totl_killed_amt DESC ) AS DECIMAL(18,4)) AS totl_killed_amt_percentage
        ,red_times
        ,dream_enter_times
        ,nightmare_enter_times
        ,nightmare_dead_times
        ,bub_count
        ,clr_bub_count
        ,bub_lost_count
        ,clr_bub_lost_count
        ,nightmare_sum_flam
        ,nightmare_max_flam
        ,per_max_flame_consume
        ,upgrade_lost_num
        ,RANK() OVER (ORDER BY amt DESC ) AS account_totl_killed_amt_rank
        ,CAST(PERCENT_RANK() OVER (ORDER BY amt DESC ) AS DECIMAL(18,4)) AS account_totl_killed_amt_percentage
        ,max_pass_s6_times
        ,item_990003_income_amount
        ,item_990004_income_amount
        ,min_15days_sanity
        ,max_15days_sanity
        ,totl_alive_days
        ,red_skill_income_amount
        ,fight_laker_times
        ,most_eaten_food
        ,most_hold_thing
        ,totl_pass_times
        ,role_id_season_max_level
        ,s7_open_amount
        ,s7_gear_amount
        ,s7_clrgear_amount
        ,s7_max_gear_once_amount
        ,s7_max_clrgear_once_amount
        ,s7_boss_battle_amount
        ,s7_spcl_event_amount
        ,s7_president_amount
        ,s8_draw_done_amount
        ,s8_max_7block_amount
        ,s8_max_7box_amount
        ,s8_sum_7egg_amount
        ,s8_sum_askill_amount
        ,s8_sum_sskill_amount
        ,s8_max_flame_amount
        ,s8_sum_flame_amount
        ,s8_sum_destory_amount
        ,CAST(PERCENT_RANK() OVER (ORDER BY s8_max_7block_amount DESC ) AS DECIMAL(18,4)) AS s8_max_7block_amount_percentage
        ,CAST(PERCENT_RANK() OVER (ORDER BY s8_max_7box_amount DESC ) AS DECIMAL(18,4)) AS s8_max_7box_amount_percentage
        ,summit_open_times
        ,summit_success_max_layer
        ,summit_max_retry_layer
        ,summit_max_retry_times
        ,s9_tarot_amount
        ,s9_tarot_enter_amount
        ,s9_tarot_dead_amount
        ,s9_dead_skill
        ,s9_dead_skill_amount
        ,s9_clr_case_once_amount
        ,s9_clr_case_amount
        ,s9_tianming_amount
        ,s9_forge_upgrade_times
        ,s9_forge_upgrade_success_times
        ,s9_forge_max_fail_times
        ,s9_forge_success_rate
        ,CAST(PERCENT_RANK() OVER (ORDER BY s9_forge_success_rate DESC ) AS DECIMAL(18,4)) AS s9_forge_success_rate_percentage
        ,s9_dead_skill
        ,s10_pals_amount
        ,s10_trade_amount
        ,s10_pillage_amount
        ,s10_carry_resus
        ,s10_max_flame_amount
        ,s10_spices_amount
        ,s10_10spices_amount
        ,s10_totl_coins_acq
        ,s10_totl_invest
        ,hijack_car_cnt
        ,bounty_complete_cnt
        ,premium_bounty_complete_cnt
        ,deep_research_success_cnt
        ,runaway_monster_kill_cnt
        ,lucky_moment_success_cnt
        ,tower_coin_gain_sum
        ,central_vault_small_chest_plunder_cnt
        ,central_vault_large_chest_open_cnt
        ,total_pass_gate_count
        ,total_enter_layer4_count
        ,total_kill_gatekeeper_count
        ,total_kill_hunter_count
        ,total_colored_bottle_count
        ,total_nixiang_count
        ,total_disturbance_count
        ,total_pickup_skull_count
        -- S13 指标
        ,s13_craving_substance_cnt
        ,s13_perfect_organ_cnt
        ,s13_scavenger_kill_cnt
        ,s13_level_open_cnt
        ,s13_level_score_max
        ,s13_level_score_min
        ,s13_colored_jar_cnt
        ,s13_max_monster_num
        ,s13_max_single_monster_score
        ,s13_most_used_modifier
        ,s13_most_used_effect
        ,s13_total_vitality
FROM    (
            SELECT  a.account AS account
                    ,CAST(a.season AS INT) AS season
                    ,d.totl_login_days AS totl_login_days
                    ,a.totl_play_mins AS totl_play_sec
                    ,c.season_login_days AS sesn_login_days
                    ,a.sesn_play_mins AS sesn_play_sec
                    ,CASE   WHEN a.season < 701 THEN jj_240705.totl_killed_amt
                            WHEN a.season >= 701 AND a.season <= 901 THEN jj_250417.totl_killed_amt
                            ELSE n.totl_killed_amt
                    END AS totl_killed_amt
                    ,b.level AS highest_hero_purchase_level
                    ,CASE   WHEN a.season < 701 THEN jj_240705.dungeon_complete_times
                            WHEN a.season >= 701 AND a.season <= 901 THEN jj_250417.dungeon_complete_times
                            ELSE n.dungeon_total_kill_num
                    END AS dungeon_complete_times
                    ,CAST(f.dungeon_plane_watcher_killed_times AS BIGINT) AS dungeon_plane_watcher_killed_times
                    ,CAST(f.dungeon_realm_lord_killed_times AS BIGINT) AS dungeon_realm_lord_killed_times
                    ,CAST(f.dungeon_keegan_killed_times + f.dungeon_pirates_killed_times + f.guwang_killed_times AS BIGINT) AS dungeon_keegan_and_pirates_killed_times
                    ,CASE   WHEN a.season < 501 THEN jj_231227.gow_open_times
                            WHEN a.season >= 501 AND a.season < 701 THEN jj_240705.gow_open_times
                            WHEN a.season >= 701 AND a.season < 801 THEN jj_241025.gow_open_times
                            WHEN a.season >= 801 AND a.season < 901 THEN jj_250109.gow_open_times
                            WHEN a.season >= 901 AND a.season < 1001 THEN jj_250417.gow_open_times
                            ELSE CAST(h.gow_open_times AS BIGINT)
                    END AS gow_open_times
                    ,CASE   WHEN a.season < 501 THEN jj_231227.gop_open_times
                            WHEN a.season >= 501 AND a.season < 701 THEN jj_240705.gop_open_times
                            WHEN a.season >= 701 AND a.season < 801 THEN jj_241025.gop_open_times
                            WHEN a.season >= 801 AND a.season < 901 THEN jj_250109.gop_open_times
                            WHEN a.season >= 901 AND a.season < 1001 THEN jj_250417.gop_open_times
                            ELSE CAST(h.gop_open_times AS BIGINT)
                    END AS gop_open_times
                    ,CASE   WHEN a.season < 501 THEN jj_231227.goh_open_times
                            WHEN a.season >= 501 AND a.season < 701 THEN jj_240705.goh_open_times
                            WHEN a.season >= 701 AND a.season < 801 THEN jj_241025.goh_open_times
                            WHEN a.season >= 801 AND a.season < 901 THEN jj_250109.goh_open_times
                            WHEN a.season >= 901 AND a.season < 1001 THEN jj_250417.goh_open_times
                            ELSE CAST(h.goh_open_times AS BIGINT)
                    END AS goh_open_times
                    ,CASE   WHEN a.season < 501 THEN jj_231227.gom_open_times
                            WHEN a.season >= 501 AND a.season < 701 THEN jj_240705.gom_open_times
                            WHEN a.season >= 701 AND a.season < 801 THEN jj_241025.gom_open_times
                            WHEN a.season >= 801 AND a.season < 901 THEN jj_250109.gom_open_times
                            WHEN a.season >= 901 AND a.season < 1001 THEN jj_250417.gom_open_times
                            ELSE CAST(h.gom_open_times AS BIGINT)
                    END AS gom_open_times
                    ,i.flame_elementium_aqr_amt
                    ,i.flame_sand_aqr_amt
                    ,i.flame_dust_aqr_amt
                    ,i.ember_aqr_amt
                    ,i.Q1 AS flame_elementium_craft_cnsum_amt
                    ,i.Q2 AS flame_sand_craft_cnsum_amt
                    ,i.Q3 AS flame_dust_craft_cnsum_amt
                    ,i.Q5 AS ember_craft_cnsum_amt
                    ,CASE   WHEN a.season < 1101 THEN jj.flame_elementium_aqr_maximum_day_amt
                            ELSE j.flame_elementium_aqr_max
                    END AS flame_elementium_aqr_maximum_day_amt
                    ,i.fluorescent_memory_aqr_amt AS fluorescent_memory_aqr_amt
                    ,i.compass_aqr_amt AS compass_aqr_amt
                    ,i.legendary_gear_aqr_amt AS legendary_gear_aqr_amt
                    ,i.other_gear_aqr_amt AS other_gear_aqr_amt
                    ,i.alevel_legendary_gear_aqr_amt AS alevel_legendary_gear_aqr_amt
                    ,i.blevel_legendary_gear_aqr_amt AS blevel_legendary_gear_aqr_amt
                    ,CASE   WHEN a.season < 501 THEN jj_231227.gear_corroded_times
                            WHEN a.season >= 501 AND a.season < 801 THEN jj_241025.gear_corroded_times
                            WHEN a.season >= 801 AND a.season < 901 THEN jj_250109.gear_corroded_times
                            WHEN a.season >= 901 AND a.season < 1001 THEN jj_250417.gear_corroded_times
                            ELSE CAST(k.totl_corrode_count AS BIGINT)
                    END AS gear_corroded_times
                    ,CASE   WHEN a.season < 501 THEN jj_231227.gear_defiled_times
                            WHEN a.season >= 501 AND a.season < 801 THEN jj_241025.gear_defiled_times
                            WHEN a.season >= 801 AND a.season < 901 THEN jj_250109.gear_defiled_times
                            WHEN a.season >= 901 AND a.season < 1001 THEN jj_250417.gear_defiled_times
                            ELSE CAST(k.totl_defiled_count AS BIGINT)
                    END AS gear_defiled_times
                    ,l.th_first_trade_date AS th_first_trade_date
                    ,l.th_total_prchs_times AS th_total_prchs_times
                    ,CASE   WHEN a.season <= 701 THEN jj_241025.th_total_sales_times
                            WHEN a.season > 701 AND a.season < 1001 THEN jj_250109.th_total_sales_times
                            ELSE l.th_total_sales_times
                    END AS th_total_sales_times
                    ,CASE   WHEN a.season <= 701 THEN jj_241025.th_flame_elementium_aqr_amt
                            WHEN a.season > 701 AND a.season < 1001 THEN jj_250109.th_flame_elementium_aqr_amt
                            ELSE l.th_flame_elementium_aqr_amt
                    END AS th_flame_elementium_aqr_amt
                    ,l.th_flame_elementium_cnsum_amt AS th_flame_elementium_cnsum_amt
                    ,CASE   WHEN a.season <= 701 THEN jj_241025.th_flame_elementium_aqr_max_amt
                            WHEN a.season > 701 AND a.season < 1001 THEN jj_250109.th_flame_elementium_aqr_max_amt
                            ELSE l.th_flame_elementium_aqr_max_amt
                    END AS th_flame_elementium_aqr_max_amt
                    ,l.th_flame_elementium_cnsum_max_amt AS th_flame_elementium_cnsum_max_amt
                    ,CASE   WHEN a.season < 501 THEN jj_231227.total_dead_times
                            WHEN a.season >= 501 AND a.season < 801 THEN jj_241025.total_dead_times
                            WHEN a.season >= 801 AND a.season < 901 THEN jj_250109.total_dead_times
                            WHEN a.season >= 901 AND a.season < 1001 THEN jj_250417.total_dead_times
                            ELSE CAST(n.death_count AS BIGINT)
                    END AS total_dead_times
                    ,0 AS appearance_amt
                    ,0 AS pactspirit_amt
                    ,0 AS in_hideout_mins
                    ,jj_230908.cube_open_times
                    ,jj_230908.greed_times
                    ,jj_230908.greed_success_times
                    ,jj_230908.divinity_count
                    ,q.complete_count AS tower_complete_count
                    ,q.total_kill_num AS tower_total_kill_num
                    ,b.role_name AS role_name_season_max_level
                    ,r.max_flame_income_ins4gameplay
                    ,r.all_flame_income_ins4gameplay
                    ,r.forever_income_ins4gameplay
                    ,r.cand_income_ins4gameplay
                    ,r.orange_times
                    ,r.mutated_times
                    ,r.infinite_difficulty_upper_limit
                    ,r.red_times
                    ,b.hero_id
                    ,s.dream_enter_times
                    ,s.nightmare_enter_times
                    ,s.nightmare_dead_times
                    ,s.bub_count
                    ,s.clr_bub_count
                    ,s.bub_lost_count
                    ,s.clr_bub_lost_count
                    ,s.nightmare_sum_flam
                    ,s.nightmare_max_flam
                    ,t.per_max_flame_consume
                    ,t.upgrade_lost_num
                    ,o2.amt AS amt
                    ,u.max_pass_s6_times
                    ,u.item_990003_income_amount
                    ,u.item_990004_income_amount
                    ,u.min_15days_sanity
                    ,u.max_15days_sanity
                    ,u.totl_alive_days
                    ,u.red_skill_income_amount
                    ,u.fight_laker_times
                    ,u.most_eaten_food
                    ,u.most_hold_thing
                    ,u.totl_pass_times
                    ,b.role_id AS role_id_season_max_level
                    ,v.s7_open_amount
                    ,v.s7_gear_amount
                    ,v.s7_clrgear_amount
                    ,v.s7_max_gear_once_amount
                    ,v.s7_max_clrgear_once_amount
                    ,v.s7_boss_battle_amount
                    ,v.s7_spcl_event_amount
                    ,v.s7_president_amount
                    ,w.s8_draw_done_amount
                    ,w.s8_max_7block_amount
                    ,w.s8_max_7box_amount
                    ,w.s8_sum_7egg_amount
                    ,w.s8_sum_askill_amount
                    ,w.s8_sum_sskill_amount
                    ,w.s8_max_flame_amount
                    ,w.s8_sum_flame_amount
                    ,w.s8_sum_destory_amount
                    ,x.summit_open_times
                    ,x.summit_success_max_layer
                    ,x.summit_max_retry_layer
                    ,x.summit_max_retry_times
                    ,kk.s9_tarot_amount
                    ,kk.s9_tarot_enter_amount
                    ,kk.s9_tarot_dead_amount
                    ,IF(kk.s9_dead_skill = '0','冥神',kk.s9_dead_skill) AS s9_dead_skill
                    ,kk.s9_dead_skill_amount
                    ,kk.s9_clr_case_once_amount
                    ,kk.s9_clr_case_amount
                    ,kk.s9_tianming_amount
                    ,ll.s9_forge_upgrade_times
                    ,NVL(ll.s9_forge_upgrade_success_times,0) AS s9_forge_upgrade_success_times
                    ,NVL(ll.s9_forge_max_fail_times,0) AS s9_forge_max_fail_times
                    ,NVL(ll.s9_forge_success_rate,0) AS s9_forge_success_rate
                    ,NVL(s10_pals_amount,0) AS s10_pals_amount
                    ,NVL(s10_trade_amount,0) AS s10_trade_amount
                    ,NVL(s10_pillage_amount,0) AS s10_pillage_amount
                    ,NVL(s10_carry_resus,0) AS s10_carry_resus
                    ,NVL(s10_max_flame_amount,0) AS s10_max_flame_amount
                    ,NVL(s10_spices_amount,0) AS s10_spices_amount
                    ,NVL(s10_10spices_amount,0) AS s10_10spices_amount
                    ,NVL(s10_totl_coins_acq,0) AS s10_totl_coins_acq
                    ,NVL(s10_totl_invest,0) AS s10_totl_invest
                    ,NVL(hijack_car_cnt,0) AS hijack_car_cnt
                    ,NVL(bounty_complete_cnt,0) AS bounty_complete_cnt
                    ,NVL(premium_bounty_complete_cnt,0) AS premium_bounty_complete_cnt
                    ,NVL(deep_research_success_cnt,0) AS deep_research_success_cnt
                    ,NVL(runaway_monster_kill_cnt,0) AS runaway_monster_kill_cnt
                    ,NVL(lucky_moment_success_cnt,0) AS lucky_moment_success_cnt
                    ,NVL(tower_coin_gain_sum,0) AS tower_coin_gain_sum
                    ,NVL(central_vault_small_chest_plunder_cnt,0) AS central_vault_small_chest_plunder_cnt
                    ,NVL(central_vault_large_chest_open_cnt,0) AS central_vault_large_chest_open_cnt
                    ,NVL(oo.total_pass_gate_count,0)          AS total_pass_gate_count
                    ,NVL(oo.total_enter_layer4_count,0)       AS total_enter_layer4_count
                    ,NVL(oo.total_kill_gatekeeper_count,0)    AS total_kill_gatekeeper_count
                    ,NVL(oo.total_kill_hunter_count,0)        AS total_kill_hunter_count
                    ,NVL(oo.total_colored_bottle_count,0)     AS total_colored_bottle_count
                    ,NVL(oo.total_nixiang_count,0)            AS total_nixiang_count
                    ,NVL(oo.total_disturbance_count,0)        AS total_disturbance_count
                    ,NVL(oo.total_pickup_skull_count,0)       AS total_pickup_skull_count
                    -- S13 指标
                    ,NVL(pp.s13_craving_substance_cnt,    0)  AS s13_craving_substance_cnt
                    ,NVL(pp.s13_perfect_organ_cnt,        0)  AS s13_perfect_organ_cnt
                    ,NVL(pp.s13_scavenger_kill_cnt,       0)  AS s13_scavenger_kill_cnt
                    ,NVL(pp.s13_level_open_cnt,           0)  AS s13_level_open_cnt
                    ,NVL(pp.s13_level_score_max,          0)  AS s13_level_score_max
                    ,NVL(pp.s13_level_score_min,          0)  AS s13_level_score_min
                    ,NVL(pp.s13_colored_jar_cnt,          0)  AS s13_colored_jar_cnt
                    ,NVL(pp.s13_max_monster_num,          0)  AS s13_max_monster_num
                    ,NVL(pp.s13_max_single_monster_score, 0)  AS s13_max_single_monster_score
                    ,NVL(pp.s13_most_used_modifier,       0)  AS s13_most_used_modifier
                    ,NVL(pp.s13_most_used_effect,         0)  AS s13_most_used_effect
                    ,NVL(pp.s13_total_vitality,           0)  AS s13_total_vitality

            FROM    (
                        SELECT  account
                                ,total_time_min AS totl_play_mins
                                ,season
                                ,season_total_time_min AS sesn_play_mins
                        FROM    tapdb_one_data.dws_torchlight_account_duration_status_df
                        WHERE   dt = '${dt}'
                    ) a
            LEFT JOIN   (
                            SELECT  account ,role_id ,role_name ,hero_id ,hero_purchase_id ,season ,level
                            FROM    (
                                        SELECT  account ,role_id ,role_name ,hero_id ,hero_purchase_id ,season ,level
                                                ,ROW_NUMBER() OVER (PARTITION BY account,season ORDER BY level DESC ) AS rn
                                        FROM    tapdb_one_data.dws_torchlight_role_status_df
                                        WHERE   dt = '${dt}' AND sid IN ('p_cn','t_MidSeason')
                                    ) WHERE rn = 1
                        ) b ON a.account = b.account AND a.season = b.season
            LEFT JOIN   (
                            SELECT  MAX(total_login_days) AS season_login_days ,account ,season
                            FROM    tapdb_one_data.dws_torchlight_role_status_df
                            WHERE   dt = '${dt}' AND sid IN ('p_cn','t_MidSeason')
                            GROUP BY account ,season
                        ) c ON a.account = c.account AND a.season = c.season
            LEFT JOIN   (
                            SELECT  SUM(total_login_day) AS totl_login_days ,account
                            FROM    (
                                        SELECT  MAX(total_login_days) AS total_login_day ,account ,season
                                        FROM    tapdb_one_data.dws_torchlight_role_status_df
                                        WHERE   dt = '${dt}' AND sid IN ('p_cn','t_MidSeason')
                                        GROUP BY account ,season
                                    )
                            GROUP BY account
                        ) d ON a.account = d.account
            LEFT JOIN   (
                            SELECT  account ,season
                                    ,SUM(CASE WHEN boss_id IN ('121202','121203','121201','151003','151004','1111012','1111014','121320','121321','121300','1000123','1000135') THEN kill_cnt_std ELSE 0 END) AS dungeon_plane_watcher_killed_times
                                    ,SUM(CASE WHEN boss_id IN ('121073','121074','121075','121080') THEN kill_cnt_std ELSE 0 END) AS dungeon_realm_lord_killed_times
                                    ,SUM(CASE WHEN boss_id IN ('9999040','9999038') THEN kill_cnt_std ELSE 0 END) AS dungeon_keegan_killed_times
                                    ,SUM(CASE WHEN boss_id IN ('1400113','1400112','1400102','130000','130001','130002') THEN kill_cnt_std ELSE 0 END) AS dungeon_pirates_killed_times
                                    ,SUM(CASE WHEN boss_id IN ('9999705','9999707','9999708') THEN kill_cnt_std ELSE 0 END) AS guwang_killed_times
                            FROM    tapdb_one_data.dws_torchlight_role_boss_battle_status_df
                            WHERE   dt = '${dt}'
                            GROUP BY account ,season
                        ) f ON a.account = f.account AND a.season = f.season
            LEFT JOIN   (
                            SELECT  account ,season
                                    ,SUM(gow_enter_times) AS gow_open_times ,SUM(gop_enter_times) AS gop_open_times
                                    ,SUM(goh_enter_times) AS goh_open_times ,SUM(gom_enter_times) AS gom_open_times
                            FROM    tapdb_one_data.dws_torchlight_gameplay_df
                            WHERE   dt = '${dt}'
                            GROUP BY account ,season
                        ) h ON a.account = h.account AND a.season = h.season
            LEFT JOIN   (
                            SELECT  account.account ,account.season
                                    ,CAST(SUM(item.flame_elementium_aqr_amt) AS BIGINT) AS flame_elementium_aqr_amt
                                    ,CAST(SUM(item.flame_sand_aqr_amt) AS BIGINT) AS flame_sand_aqr_amt
                                    ,CAST(SUM(item.flame_dust_aqr_amt) AS BIGINT) AS flame_dust_aqr_amt
                                    ,CAST(SUM(item.ember_aqr_amt) AS BIGINT) AS ember_aqr_amt
                                    ,CAST(SUM(q1) AS BIGINT) AS Q1 ,CAST(SUM(q2) AS BIGINT) AS Q2
                                    ,CAST(SUM(q3) AS BIGINT) AS Q3 ,CAST(SUM(q5) AS BIGINT) AS Q5
                                    ,CAST(SUM(compass_aqr_amt) AS BIGINT) AS compass_aqr_amt
                                    ,CAST(SUM(fluorescent_memory_aqr_amt) AS BIGINT) AS fluorescent_memory_aqr_amt
                                    ,CAST(SUM(alevel_legendary_gear_aqr_amt) AS BIGINT) AS alevel_legendary_gear_aqr_amt
                                    ,CAST(SUM(blevel_legendary_gear_aqr_amt) AS BIGINT) AS blevel_legendary_gear_aqr_amt
                                    ,CAST(SUM(legendary_gear_aqr_amt) AS BIGINT) AS legendary_gear_aqr_amt
                                    ,CAST(SUM(other_gear_aqr_amt) AS BIGINT) AS other_gear_aqr_amt
                            FROM    (SELECT account ,role_id ,season FROM tapdb_one_data.dws_torchlight_role_status_df WHERE dt = '${dt}') account
                            LEFT JOIN (
                                            SELECT  fact.role_id
                                                    ,SUM(IF(fact.item_id = 100300,fact.item_income_std,0)) AS flame_elementium_aqr_amt
                                                    ,SUM(IF(fact.item_id = 100200,fact.item_income_std,0)) AS flame_sand_aqr_amt
                                                    ,SUM(IF(fact.item_id = 100100,fact.item_income_std,0)) AS flame_dust_aqr_amt
                                                    ,SUM(IF(fact.item_id = 100400,fact.item_income_std,0)) AS flame_residues_aqr_amt
                                                    ,SUM(IF(dim_item.type = 15,fact.item_income_std,0)) AS ember_aqr_amt
                                                    ,SUM(IF(fact.item_id = 100300 AND via IN (11001,11002,11006,11008,11009,11010,11011),fact.item_consume_std,0)) AS q1
                                                    ,SUM(IF(fact.item_id = 100200 AND via IN (11001,11002,11006,11008,11009,11010,11011),fact.item_consume_std,0)) AS q2
                                                    ,SUM(IF(fact.item_id = 100100 AND via IN (11001,11002,11006,11008,11009,11010,11011),fact.item_consume_std,0)) AS q3
                                                    ,SUM(IF(fact.item_id = 100400 AND via IN (11001,11002,11006,11008,11009,11010,11011),fact.item_consume_std,0)) AS q4
                                                    ,SUM(IF(dim_item.type = 15 AND via IN (11001,11002,11006,11008,11009,11010,11011),fact.item_consume_std,0)) AS q5
                                                    ,SUM(IF(dim_item.name LIKE '%罗盘%',fact.item_income_std,0)) AS compass_aqr_amt
                                                    ,SUM(IF(dim_item.type_name = '命运卡',fact.item_income_std,0)) AS fluorescent_memory_aqr_amt
                                                    ,SUM(IF(dim_gold.rarity_level = 1,fact.item_income_std,0)) AS alevel_legendary_gear_aqr_amt
                                                    ,SUM(IF(dim_gold.rarity_level = 2,fact.item_income_std,0)) AS blevel_legendary_gear_aqr_amt
                                                    ,SUM(IF(dim_gold.rarity_level IN (3,4,5,6),fact.item_income_std,0)) AS legendary_gear_aqr_amt
                                                    ,SUM(IF(fact.item_gold_id = 0 AND dim_item.type_name = '装备',fact.item_income_std,0)) AS other_gear_aqr_amt
                                            FROM    (SELECT DISTINCT role_id,item_id,via,pid,item_income_std,item_consume_std,item_income_td,item_consume_td,item_gold_id,item_drop_source,sid,season_label,item_income_times,item_consume_times,dt
                                                     FROM tapdb_one_data.dws_torchlight_role_item_df WHERE dt = '${dt}' AND via NOT IN ('20002','20001') AND sid IN ('p_cn','t_MidSeason')) fact
                                            LEFT JOIN tapdb_one_data.dim_torchlight_item_name_type dim_item ON fact.item_id = dim_item.id
                                            LEFT JOIN tapdb_one_data.dim_torchlight_item_gold_name dim_gold ON fact.item_gold_id = dim_gold.id
                                            GROUP BY fact.role_id
                                        ) item ON item.role_id = account.role_id
                            GROUP BY account.account ,account.season
                        ) i ON a.account = i.account AND a.season = i.season
            LEFT JOIN   (
                            SELECT  account ,season ,MAX(flame_elementium_aqr_max) AS flame_elementium_aqr_max
                            FROM    tapdb_one_data.dws_torchlight_paramount_max_df
                            GROUP BY account ,season
                        ) j ON a.account = j.account AND a.season = j.season
            LEFT JOIN   (
                            SELECT  account ,season
                                    ,CAST(SUM(totl_corrode_count) AS BIGINT) AS totl_corrode_count
                                    ,CAST(SUM(totl_defiled_count) AS BIGINT) AS totl_defiled_count
                            FROM    tapdb_one_data.dws_torchlight_equipment_corrode_df
                            WHERE   dt = '${dt}'
                            GROUP BY account ,season
                        ) k ON a.account = k.account AND a.season = k.season
            LEFT JOIN   (
                            SELECT  account ,season
                                    ,MIN(th_first_trade_date) AS th_first_trade_date
                                    ,CAST(SUM(th_total_prchs_times) AS BIGINT) AS th_total_prchs_times
                                    ,CAST(SUM(th_total_sales_times) AS BIGINT) AS th_total_sales_times
                                    ,CAST(SUM(th_flame_elementium_aqr_amt) AS BIGINT) AS th_flame_elementium_aqr_amt
                                    ,CAST(SUM(th_flame_elementium_cnsum_amt) AS BIGINT) AS th_flame_elementium_cnsum_amt
                                    ,CAST(SUM(th_flame_elementium_aqr_max_amt) AS BIGINT) AS th_flame_elementium_aqr_max_amt
                                    ,CAST(SUM(th_flame_elementium_cnsum_max_amt) AS BIGINT) AS th_flame_elementium_cnsum_max_amt
                            FROM    tapdb_one_data.dws_torchlight_exchange_trade_snapshot_df
                            WHERE   dt = '${dt}'
                            GROUP BY account ,season
                        ) l ON a.account = l.account AND a.season = l.season
            LEFT JOIN   (
                            SELECT  account ,season
                                    ,SUM(totl_killed_amt) AS totl_killed_amt ,SUM(total_kill_num) AS total_kill_num
                                    ,SUM(dungeon_total_kill_num) AS dungeon_total_kill_num ,SUM(death_count) AS death_count
                            FROM    tapdb_one_data.dws_torchlight_account_battle_di
                            WHERE   dt = '${dt}'
                            GROUP BY account ,season
                        ) n ON a.account = n.account AND a.season = n.season
            LEFT JOIN   (
                            SELECT  account ,SUM(totl_killed_amt) + SUM(total_kill_num) AS amt
                            FROM    tapdb_one_data.dws_torchlight_account_battle_di
                            WHERE   dt = '${dt}'
                            GROUP BY account
                        ) o2 ON a.account = o2.account
            LEFT JOIN   (
                            SELECT  account ,season ,SUM(complete_count) AS complete_count ,SUM(total_kill_num) AS total_kill_num
                            FROM    tapdb_one_data.dws_torchlight_role_tower_di
                            WHERE   dt >= '2023-05-10'
                            GROUP BY account ,season
                        ) q ON a.account = q.account AND a.season = q.season
            LEFT JOIN   (
                            SELECT  account ,season ,max_flame_income_ins4gameplay ,all_flame_income_ins4gameplay
                                    ,forever_income_ins4gameplay ,cand_income_ins4gameplay ,orange_times ,mutated_times
                                    ,infinite_difficulty_upper_limit ,red_times
                            FROM    tapdb_one_data.dws_torchlight_account_career_df
                            WHERE   dt = '2023-12-27' AND season IN (401,411,421,431,441)
                        ) r ON a.account = r.account AND a.season = r.season
            LEFT JOIN   (
                            SELECT  account ,season
                                    ,SUM(dream_enter_times) AS dream_enter_times ,SUM(nightmare_enter_times) AS nightmare_enter_times
                                    ,SUM(nightmare_dead_times) AS nightmare_dead_times ,SUM(bub_count) AS bub_count
                                    ,SUM(clr_bub_count) AS clr_bub_count ,SUM(bub_lost_count) AS bub_lost_count
                                    ,SUM(clr_bub_lost_count) AS clr_bub_lost_count ,SUM(nightmare_sum_flam) AS nightmare_sum_flam
                                    ,MAX(nightmare_max_flam) AS nightmare_max_flam
                            FROM    tapdb_one_data.dws_torchlight_role_s5gameplay_f
                            WHERE   dt = '2024-04-17'
                            GROUP BY account ,season
                        ) s ON a.account = s.account AND a.season = s.season
            LEFT JOIN   (
                            SELECT  account ,season ,MAX(per_max_flame_consume) AS per_max_flame_consume ,SUM(upgrade_lost_num) AS upgrade_lost_num
                            FROM    tapdb_one_data.dws_torchlight_role_forge_df
                            WHERE   dt = '${dt}'
                            GROUP BY account ,season
                        ) t ON a.account = t.account AND a.season = t.season
            LEFT JOIN   (
                            SELECT  account ,season
                                    ,MAX(max_pass_s6_times) AS max_pass_s6_times ,SUM(item_990003_income_amount) AS item_990003_income_amount
                                    ,SUM(item_990004_income_amount) AS item_990004_income_amount ,MIN(min_15days_sanity) AS min_15days_sanity
                                    ,MAX(max_15days_sanity) AS max_15days_sanity ,SUM(totl_alive_days) AS totl_alive_days
                                    ,SUM(red_skill_income_amount) AS red_skill_income_amount ,SUM(fight_laker_times) AS fight_laker_times
                                    ,MAX(most_eaten_food) AS most_eaten_food ,MAX(most_hold_thing) AS most_hold_thing ,SUM(totl_pass_times) AS totl_pass_times
                            FROM    tapdb_one_data.dws_torchlight_role_s6gameplay_df
                            WHERE   dt = '2024-07-04' AND sid = 'p_cn'
                            GROUP BY account ,season
                        ) u ON a.account = u.account AND a.season = u.season
            LEFT JOIN   (
                            SELECT  account ,season
                                    ,MAX(s7_open_amount) AS s7_open_amount ,MAX(s7_gear_amount) AS s7_gear_amount
                                    ,MAX(s7_clrgear_amount) AS s7_clrgear_amount ,MAX(s7_max_gear_once_amount) AS s7_max_gear_once_amount
                                    ,MAX(s7_max_clrgear_once_amount) AS s7_max_clrgear_once_amount ,MAX(s7_boss_battle_amount) AS s7_boss_battle_amount
                                    ,MAX(s7_spcl_event_amount) AS s7_spcl_event_amount ,MAX(s7_president_amount) AS s7_president_amount
                            FROM    tapdb_one_data.dws_torchlight_s7gameplay_di
                            WHERE   dt = '2024-10-24'
                            GROUP BY account ,season
                        ) v ON a.account = v.account AND a.season = v.season
            LEFT JOIN   (
                            SELECT  account ,season
                                    ,MAX(s8_draw_done_amount) AS s8_draw_done_amount ,MAX(s8_max_7block_amount) AS s8_max_7block_amount
                                    ,MAX(s8_max_7box_amount) AS s8_max_7box_amount ,MAX(s8_sum_7egg_amount) AS s8_sum_7egg_amount
                                    ,MAX(s8_sum_askill_amount) AS s8_sum_askill_amount ,MAX(s8_sum_sskill_amount) AS s8_sum_sskill_amount
                                    ,MAX(s8_max_flame_amount) AS s8_max_flame_amount ,MAX(s8_sum_flame_amount) AS s8_sum_flame_amount
                                    ,MAX(s8_sum_destory_amount) AS s8_sum_destory_amount
                            FROM    tapdb_one_data.dws_torchlight_s8gameplay_di
                            WHERE   dt = '2025-01-08'
                            GROUP BY account ,season
                        ) w ON a.account = w.account AND a.season = w.season
            LEFT JOIN   (
                            SELECT  account ,season
                                    ,MAX(summit_open_times) AS summit_open_times ,MAX(summit_success_max_layer) AS summit_success_max_layer
                                    ,MAX(summit_max_retry_layer) AS summit_max_retry_layer ,MAX(summit_max_retry_times) AS summit_max_retry_times
                            FROM    tapdb_one_data.dws_torchlight_summit_race_di
                            WHERE   dt = '${dt}'
                            GROUP BY account ,season
                        ) x ON a.account = x.account AND a.season = x.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(s9_tarot_amount) AS s9_tarot_amount ,MAX(s9_tarot_enter_amount) AS s9_tarot_enter_amount
                                    ,MAX(s9_tarot_dead_amount) AS s9_tarot_dead_amount ,MAX(s9_dead_skill) AS s9_dead_skill
                                    ,MAX(s9_dead_skill_amount) AS s9_dead_skill_amount ,MAX(s9_clr_case_once_amount) AS s9_clr_case_once_amount
                                    ,MAX(s9_clr_case_amount) AS s9_clr_case_amount ,MAX(s9_tianming_amount) AS s9_tianming_amount
                            FROM    tapdb_one_data.dws_torchlight_s9gameplay_di
                            WHERE   dt = '2025-04-17'
                            GROUP BY season ,account
                        ) kk ON a.account = kk.account AND a.season = kk.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(s9_forge_upgrade_times) AS s9_forge_upgrade_times
                                    ,MAX(s9_forge_upgrade_success_times) AS s9_forge_upgrade_success_times
                                    ,MAX(s9_forge_max_fail_times) AS s9_forge_max_fail_times
                                    ,MAX(s9_forge_success_rate) AS s9_forge_success_rate
                            FROM    tapdb_one_data.dws_torchlight_s9_equipment_forge_di
                            WHERE   dt = '${dt}'
                            GROUP BY season ,account
                        ) ll ON a.account = ll.account AND a.season = ll.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(s10_pals_amount) AS s10_pals_amount ,MAX(s10_trade_amount) AS s10_trade_amount
                                    ,MAX(s10_pillage_amount) AS s10_pillage_amount ,MAX(s10_carry_resus) AS s10_carry_resus
                                    ,MAX(s10_max_flame_amount) AS s10_max_flame_amount ,MAX(s10_spices_amount) AS s10_spices_amount
                                    ,MAX(s10_10spices_amount) AS s10_10spices_amount ,MAX(s10_totl_coins_acq) AS s10_totl_coins_acq
                                    ,MAX(s10_totl_invest) AS s10_totl_invest
                            FROM    tapdb_one_data.dws_torchlight_s10gameplay_df
                            WHERE   dt = '2025-07-17'
                            GROUP BY season ,account
                        ) mm ON a.account = mm.account AND a.season = mm.season
            LEFT JOIN   (
                            SELECT  season ,account ,MAX(flame_elementium_aqr_maximum_day_amt) AS flame_elementium_aqr_maximum_day_amt
                            FROM    tapdb_one_data.dws_torchlight_account_career_df
                            WHERE   dt = '2025-07-07'
                            GROUP BY season ,account
                        ) jj ON a.account = jj.account AND a.season = jj.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(totl_killed_amt) AS totl_killed_amt ,MAX(dungeon_complete_times) AS dungeon_complete_times
                                    ,MAX(gow_open_times) AS gow_open_times ,MAX(gop_open_times) AS gop_open_times
                                    ,MAX(goh_open_times) AS goh_open_times ,MAX(gom_open_times) AS gom_open_times
                                    ,MAX(total_dead_times) AS total_dead_times ,MAX(gear_corroded_times) AS gear_corroded_times ,MAX(gear_defiled_times) AS gear_defiled_times
                            FROM    tapdb_one_data.dws_torchlight_account_career_df WHERE dt = '2023-12-28'
                            GROUP BY season ,account
                        ) jj_231227 ON a.account = jj_231227.account AND a.season = jj_231227.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(totl_killed_amt) AS totl_killed_amt ,MAX(dungeon_complete_times) AS dungeon_complete_times
                                    ,MAX(gow_open_times) AS gow_open_times ,MAX(gop_open_times) AS gop_open_times
                                    ,MAX(goh_open_times) AS goh_open_times ,MAX(gom_open_times) AS gom_open_times
                                    ,MAX(total_dead_times) AS total_dead_times ,MAX(gear_corroded_times) AS gear_corroded_times ,MAX(gear_defiled_times) AS gear_defiled_times
                                    ,MAX(th_total_sales_times) AS th_total_sales_times ,MAX(th_flame_elementium_aqr_amt) AS th_flame_elementium_aqr_amt
                                    ,MAX(th_flame_elementium_aqr_max_amt) AS th_flame_elementium_aqr_max_amt
                            FROM    tapdb_one_data.dws_torchlight_account_career_df WHERE dt = '2025-04-17'
                            GROUP BY season ,account
                        ) jj_250417 ON a.account = jj_250417.account AND a.season = jj_250417.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(totl_killed_amt) AS totl_killed_amt ,MAX(dungeon_complete_times) AS dungeon_complete_times
                                    ,MAX(gow_open_times) AS gow_open_times ,MAX(gop_open_times) AS gop_open_times
                                    ,MAX(goh_open_times) AS goh_open_times ,MAX(gom_open_times) AS gom_open_times
                                    ,MAX(gear_corroded_times) AS gear_corroded_times ,MAX(gear_defiled_times) AS gear_defiled_times
                            FROM    tapdb_one_data.dws_torchlight_account_career_df WHERE dt = '2024-07-05'
                            GROUP BY season ,account
                        ) jj_240705 ON a.account = jj_240705.account AND a.season = jj_240705.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(totl_killed_amt) AS totl_killed_amt ,MAX(dungeon_complete_times) AS dungeon_complete_times
                                    ,MAX(gow_open_times) AS gow_open_times ,MAX(gop_open_times) AS gop_open_times
                                    ,MAX(goh_open_times) AS goh_open_times ,MAX(gom_open_times) AS gom_open_times
                                    ,MAX(total_dead_times) AS total_dead_times ,MAX(gear_corroded_times) AS gear_corroded_times ,MAX(gear_defiled_times) AS gear_defiled_times
                                    ,MAX(th_total_sales_times) AS th_total_sales_times ,MAX(th_flame_elementium_aqr_amt) AS th_flame_elementium_aqr_amt
                                    ,MAX(th_flame_elementium_aqr_max_amt) AS th_flame_elementium_aqr_max_amt
                            FROM    tapdb_one_data.dws_torchlight_account_career_df WHERE dt = '2024-10-25'
                            GROUP BY season ,account
                        ) jj_241025 ON a.account = jj_241025.account AND a.season = jj_241025.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(totl_killed_amt) AS totl_killed_amt ,MAX(dungeon_complete_times) AS dungeon_complete_times
                                    ,MAX(gow_open_times) AS gow_open_times ,MAX(gop_open_times) AS gop_open_times
                                    ,MAX(goh_open_times) AS goh_open_times ,MAX(gom_open_times) AS gom_open_times
                                    ,MAX(total_dead_times) AS total_dead_times ,MAX(gear_corroded_times) AS gear_corroded_times ,MAX(gear_defiled_times) AS gear_defiled_times
                                    ,MAX(th_total_sales_times) AS th_total_sales_times ,MAX(th_flame_elementium_aqr_amt) AS th_flame_elementium_aqr_amt
                                    ,MAX(th_flame_elementium_aqr_max_amt) AS th_flame_elementium_aqr_max_amt
                            FROM    tapdb_one_data.dws_torchlight_account_career_df WHERE dt = '2025-01-09'
                            GROUP BY season ,account
                        ) jj_250109 ON a.account = jj_250109.account AND a.season = jj_250109.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(totl_killed_amt) AS totl_killed_amt ,MAX(dungeon_complete_times) AS dungeon_complete_times
                                    ,MAX(gow_open_times) AS gow_open_times ,MAX(gop_open_times) AS gop_open_times
                                    ,MAX(goh_open_times) AS goh_open_times ,MAX(gom_open_times) AS gom_open_times
                                    ,MAX(cube_open_times) AS cube_open_times ,MAX(greed_times) AS greed_times
                                    ,MAX(greed_success_times) AS greed_success_times ,MAX(divinity_count) AS divinity_count
                                    ,MAX(gear_corroded_times) AS gear_corroded_times ,MAX(gear_defiled_times) AS gear_defiled_times
                            FROM    tapdb_one_data.dws_torchlight_account_career_df WHERE dt = '2023-09-08'
                            GROUP BY season ,account
                        ) jj_230908 ON a.account = jj_230908.account AND a.season = jj_230908.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(hijack_car_cnt)                        AS hijack_car_cnt
                                    ,MAX(bounty_complete_cnt)                   AS bounty_complete_cnt
                                    ,MAX(premium_bounty_complete_cnt)           AS premium_bounty_complete_cnt
                                    ,MAX(deep_research_success_cnt)             AS deep_research_success_cnt
                                    ,MAX(runaway_monster_kill_cnt)              AS runaway_monster_kill_cnt
                                    ,MAX(lucky_moment_success_cnt)              AS lucky_moment_success_cnt
                                    ,MAX(tower_coin_gain_sum)                   AS tower_coin_gain_sum
                                    ,MAX(central_vault_small_chest_plunder_cnt) AS central_vault_small_chest_plunder_cnt
                                    ,MAX(central_vault_large_chest_open_cnt)    AS central_vault_large_chest_open_cnt
                            FROM    tapdb_one_data.dws_torchlight_s11_metrics_df
                            WHERE   dt = '${dt}'
                            GROUP BY season ,account
                        ) nn ON a.account = nn.account AND a.season = nn.season
            LEFT JOIN   (
                            SELECT  season ,account
                                    ,MAX(total_pass_gate_count)         AS total_pass_gate_count
                                    ,MAX(total_enter_layer4_count)      AS total_enter_layer4_count
                                    ,MAX(total_kill_gatekeeper_count)   AS total_kill_gatekeeper_count
                                    ,MAX(total_kill_hunter_count)       AS total_kill_hunter_count
                                    ,MAX(total_colored_bottle_count)    AS total_colored_bottle_count
                                    ,MAX(total_nixiang_count)           AS total_nixiang_count
                                    ,MAX(total_disturbance_count)       AS total_disturbance_count
                                    ,MAX(total_pickup_skull_count)      AS total_pickup_skull_count
                            FROM    tapdb_one_data.dws_torchlight_s12gameplay_df
                            WHERE   dt = '${dt}'
                            GROUP BY season ,account
                        ) oo ON a.account = oo.account AND a.season = oo.season
            -- ----------------------------------------------------------------
            -- S13 指标：终局玩法 / 渴瘾物质 / 完美器官 / 清道夫 / 活性
            -- ----------------------------------------------------------------
            LEFT JOIN   (
                            SELECT  account
                                    ,season
                                    ,MAX(craving_substance_cnt)    AS s13_craving_substance_cnt
                                    ,MAX(perfect_organ_cnt)        AS s13_perfect_organ_cnt
                                    ,MAX(scavenger_kill_cnt)       AS s13_scavenger_kill_cnt
                                    ,MAX(level_open_cnt)           AS s13_level_open_cnt
                                    ,MAX(level_score_max)          AS s13_level_score_max
                                    ,MAX(level_score_min)          AS s13_level_score_min
                                    ,MAX(colored_jar_cnt)          AS s13_colored_jar_cnt
                                    ,MAX(max_monster_num)          AS s13_max_monster_num
                                    ,MAX(max_single_monster_score) AS s13_max_single_monster_score
                                    ,MAX(most_used_modifier)       AS s13_most_used_modifier
                                    ,MAX(most_used_effect)         AS s13_most_used_effect
                                    ,MAX(total_vitality)           AS s13_total_vitality
                            FROM    tapdb_one_data.dws_torchlight_s13gameplay_df
                            WHERE   dt = '${dt}'
                            GROUP BY account ,season
                        ) pp ON a.account = pp.account AND a.season = pp.season
        )
;
