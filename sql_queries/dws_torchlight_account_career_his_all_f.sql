--odps sql
--********************************************************************--
--author:蔡圣哲
--create time:2023-06-05 16:47:00
--********************************************************************--
USE tapdb_one_data
;

SET odps.sql.hive.compatible = true
;

SET odps.stage.reducer.mem = 16384
;

CREATE TABLE IF NOT EXISTS tapdb_one_data.dws_torchlight_account_career_his_all_f
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
    ,s_label                                 STRING COMMENT '赛季标签'
)
STORED AS ALIORC
;


-- ALTER TABLE tapdb_one_data.dws_torchlight_account_career_his_all_f
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
--         total_pass_gate_count           BIGINT COMMENT '累计通过叠界门次数'
--         ,total_enter_layer4_count       BIGINT COMMENT '累计进入叠界第4层次数'
--         ,total_kill_gatekeeper_count    BIGINT COMMENT '累计击杀守门人次数'
--         ,total_kill_hunter_count        BIGINT COMMENT '累计击杀狩门人次数'
--         ,total_colored_bottle_count     BIGINT COMMENT '累计获得彩色瓶中叠影数量'
--         ,total_nixiang_count            BIGINT COMMENT '累计掉落逆像数量'
--         ,total_disturbance_count        BIGINT COMMENT '累计遭遇叠界扰动次数'
--         ,total_pickup_skull_count       BIGINT COMMENT '累计捡起漂浮头颅数量'
-- );


INSERT OVERWRITE TABLE tapdb_one_data.dws_torchlight_account_career_his_all_f
-- ---------------------------------------------------------------- S3
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S3' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '2023-09-07'
UNION ALL
-- ---------------------------------------------------------------- S4
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S4' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '2023-12-27'
UNION ALL
-- ---------------------------------------------------------------- S5
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S5' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '2024-04-17'
UNION ALL
-- ---------------------------------------------------------------- S6
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S6' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '2024-07-04'
UNION ALL
-- ---------------------------------------------------------------- S7
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S7' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '2024-10-24'
UNION ALL
-- ---------------------------------------------------------------- S8
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S8' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '2025-01-08'
UNION ALL
-- ---------------------------------------------------------------- S9
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S9' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '2025-04-17'
UNION ALL
-- ---------------------------------------------------------------- S10
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S10' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '2025-09-09'
UNION ALL
-- ---------------------------------------------------------------- S11  赛季结束快照 2025-10-10
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S11' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '2025-10-10' AND season >= 1101 AND season < 1201
UNION ALL
-- ---------------------------------------------------------------- S12  赛季结束快照 2026-01-16
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S12' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '2026-01-16' AND season >= 1201 AND season < 1301
UNION ALL
-- ---------------------------------------------------------------- S13  当前赛季，使用 ${dt} 每日更新
SELECT  account
        ,season
        ,totl_login_days,totl_play_sec,sesn_login_days,sesn_play_sec,totl_killed_amt,highest_hero_purchase_level,dungeon_complete_times,dungeon_plane_watcher_killed_times,dungeon_realm_lord_killed_times,dungeon_keegan_and_pirates_killed_times,gow_open_times,gop_open_times,goh_open_times,gom_open_times,flame_elementium_aqr_amt,flame_sand_aqr_amt,flame_dust_aqr_amt,ember_aqr_amt,flame_elementium_craft_cnsum_amt,flame_sand_craft_cnsum_amt,flame_dust_craft_cnsum_amt,ember_craft_cnsum_amt,flame_elementium_aqr_maximum_day_amt,fluorescent_memory_aqr_amt,compass_aqr_amt,legendary_gear_aqr_amt,other_gear_aqr_amt,alevel_legendary_gear_aqr_amt,blevel_legendary_gear_aqr_amt,gear_corroded_times,gear_defiled_times,th_first_trade_date,th_total_prchs_times,th_total_sales_times,th_flame_elementium_aqr_amt,th_flame_elementium_cnsum_amt,th_flame_elementium_aqr_max_amt,th_flame_elementium_cnsum_max_amt,total_dead_times,appearance_amt,pactspirit_amt,in_hideout_mins,cube_open_times,greed_times,greed_success_times,divinity_count,tower_complete_count,tower_total_kill_num,role_name_season_max_level,max_flame_income_ins4gameplay,all_flame_income_ins4gameplay,forever_income_ins4gameplay,cand_income_ins4gameplay,orange_times,mutated_times,infinite_difficulty_upper_limit,totl_killed_amt_rank,dungeon_complete_times_percentage,totl_killed_amt_percentage,red_times,dream_enter_times,nightmare_enter_times,nightmare_dead_times,bub_count,clr_bub_count,bub_lost_count,clr_bub_lost_count,nightmare_sum_flam,nightmare_max_flam,per_max_flame_consume,upgrade_lost_num,account_totl_killed_amt_rank,account_totl_killed_amt_percentage,max_pass_s6_times,item_990003_income_amount,item_990004_income_amount,min_15days_sanity,max_15days_sanity,totl_alive_days,red_skill_income_amount,fight_laker_times,most_eaten_food,most_hold_thing,totl_pass_times,role_id_season_max_level,s7_open_amount,s7_gear_amount,s7_clrgear_amount,s7_max_gear_once_amount,s7_max_clrgear_once_amount,s7_boss_battle_amount,s7_spcl_event_amount,s7_president_amount,s8_draw_done_amount,s8_max_7block_amount,s8_max_7box_amount,s8_sum_7egg_amount,s8_sum_askill_amount,s8_sum_sskill_amount,s8_max_flame_amount,s8_sum_flame_amount,s8_sum_destory_amount,s8_max_7block_amount_percentage,s8_max_7box_amount_percentage,summit_open_times,summit_success_max_layer,summit_max_retry_layer,summit_max_retry_times,s9_tarot_amount,s9_tarot_enter_amount,s9_tarot_dead_amount,s9_dead_skill_percentage,s9_dead_skill_amount,s9_clr_case_once_amount,s9_clr_case_amount,s9_tianming_amount,s9_forge_upgrade_times,s9_forge_upgrade_success_times,s9_forge_max_fail_times,s9_forge_success_rate,s9_forge_success_rate_rank,s9_dead_skill,s10_pals_amount,s10_trade_amount,s10_pillage_amount,s10_carry_resus,s10_max_flame_amount,s10_spices_amount,s10_10spices_amount,s10_totl_coins_acq,s10_totl_invest
        ,'S13' AS s_label
        ,hijack_car_cnt,bounty_complete_cnt,premium_bounty_complete_cnt,deep_research_success_cnt,runaway_monster_kill_cnt,lucky_moment_success_cnt,tower_coin_gain_sum,central_vault_small_chest_plunder_cnt,central_vault_large_chest_open_cnt,total_pass_gate_count ,total_enter_layer4_count ,total_kill_gatekeeper_count ,total_kill_hunter_count ,total_colored_bottle_count ,total_nixiang_count ,total_disturbance_count ,total_pickup_skull_count
FROM    tapdb_one_data.dws_torchlight_account_career_df
WHERE   dt = '${dt}' AND season >= 1301 AND season < 1401
;
