--odps sql
--********************************************************************--
--author:蔡圣哲
--create time:2023-07-03 17:44:54
--********************************************************************--
-- DROP TABLE IF EXISTS tapdb_one_data.dwd_torchlight_exposure_di;
CREATE TABLE IF NOT EXISTS tapdb_one_data.dwd_torchlight_exposure_di
(
    account            STRING COMMENT '账号'
    ,activity_id       BIGINT COMMENT '活动id 或卡池id'
    ,app_version       STRING COMMENT '游戏版本'
    ,battery           BIGINT COMMENT '电量'
    ,box_id_type_list  STRING COMMENT '卡池'
    -- ,box_id            BIGINT COMMENT '卡池ID'
    -- ,box_type          STRING COMMENT '卡池类型'
    ,brand             STRING COMMENT '手机品牌'
    ,channel           STRING COMMENT '渠道'
    ,device_id         STRING COMMENT '设备ID'
    ,enter_channel     STRING COMMENT '主入口'
    ,event_index       BIGINT COMMENT '事件序号'
    ,exposure_index    STRING COMMENT '活动id所在左侧list顺序'
    ,game_platform     STRING COMMENT '游戏平台'
    ,gpu               STRING COMMENT 'GPU'
    ,height            INT COMMENT '屏幕高度'
    ,hero_id           BIGINT COMMENT '英雄ID'
    ,hero_purchase_id  BIGINT COMMENT '英雄专精ID'
    ,ip                STRING COMMENT 'IP'
    ,item_id           STRING COMMENT '用户所点击商品id'
    ,lang              STRING COMMENT '字体'
    ,language          STRING COMMENT '语言'
    ,level             BIGINT COMMENT '角色等级'
    ,logid             STRING COMMENT '日志唯一ID'
    ,login_type        STRING COMMENT '登录方式'
    ,`model`           STRING COMMENT '机型'
    ,name              STRING COMMENT 'exposure_constratin,面板强弹;exposure_store_click,商城商品点击;exposure_awaken,觉醒界面曝光'
    ,network           STRING COMMENT '网络类型'
    ,open_index        STRING COMMENT '本次触发强弹时第x个曝光面板'
    ,orientation       STRING COMMENT '屏幕方向'
    ,os                STRING COMMENT '操作系统'
    ,os_version        STRING COMMENT '操作系统版本'
    ,page_id           STRING COMMENT '商城内页面id'
    ,pid               STRING COMMENT '游戏账号'
    ,platform          STRING COMMENT '游戏平台'
    ,role_id           STRING COMMENT '角色ID'
    ,season            BIGINT COMMENT '赛季'
    ,session_uuid      STRING COMMENT '赛季UUID'
    ,sid               STRING COMMENT '服ID'
    ,source            STRING COMMENT '日志来源'
    ,structure         STRING COMMENT '架构'
    ,sub_enter_channel STRING COMMENT '同一来源模块id下的细分进入方式'
    ,time              TIMESTAMP COMMENT '时间'
    ,unique_id         STRING COMMENT '本次曝光唯一id'
    ,width             INT COMMENT '屏幕宽度'
    ,xdid              STRING COMMENT '心动ID'
    ,user_id           STRING COMMENT '用户ID'
    ,ip_admin_code     STRING COMMENT '根据ip解析'
    ,ip_city           STRING COMMENT '根据ip解析城市'
    ,ip_country        STRING COMMENT '根据ip解析的国家'
    ,ip_country_code   STRING COMMENT '根据ip解析的国家码'
    ,ip_isp            STRING COMMENT '根据ip解析isp'
    ,ip_latitude       DOUBLE COMMENT '根据ip解析的经纬度'
    ,ip_longitude      DOUBLE COMMENT '根据ip解析的经纬度'
    ,ip_province       STRING COMMENT '根据ip解析的省份'
    ,awaken_item_info  STRING COMMENT '觉醒界面曝光时当前持有觉醒材料数量 (exposure_awaken)'

)
PARTITIONED BY
(
    dt                 STRING COMMENT '业务日期, yyyy-mm-dd'
)
STORED AS ALIORC
TBLPROPERTIES ('comment' = '每日曝光事件明细')
LIFECYCLE 365
;

-- alter table tapdb_one_data.dwd_torchlight_exposure_di add columns (
--     box_id bigint comment '卡池ID'
--     ,box_type bigint comment '卡池类型'
-- );

-- alter table tapdb_one_data.dwd_torchlight_exposure_di add columns (
--     awaken_item_info STRING COMMENT '觉醒界面曝光时当前持有觉醒材料数量 (exposure_awaken)'
-- );

SET odps.sql.hive.compatible = TRUE
;

INSERT OVERWRITE TABLE tapdb_one_data.dwd_torchlight_exposure_di PARTITION (dt = '${dt}')
SELECT  account
        ,CAST(activity_id AS BIGINT) AS activity_id
        ,app_version
        ,battery
        ,box_id_type_list
        -- ,CAST(GET_JSON_OBJECT(exps,'$.box_id')AS BIGINT) AS box_id
        -- ,GET_JSON_OBJECT(exps,'$.box_type') AS box_type
        ,brand
        ,channel
        ,device_id
        ,enter_channel
        ,event_index
        ,exposure_index
        ,game_platform
        ,gpu
        ,height
        ,hero_id
        ,hero_purchase_id
        ,ip
        ,item_id
        ,lang
        ,language
        ,level
        ,logid
        ,login_type
        ,`model`
        ,name
        ,network
        ,open_index
        ,orientation
        ,os
        ,os_version
        ,page_id
        ,pid
        ,platform
        ,role_id
        ,season
        ,session_uuid
        ,sid
        ,source
        ,structure
        ,sub_enter_channel
        ,FROM_UTC_TIMESTAMP(CAST(RPAD(time,13,'0') AS BIGINT),'UTC') AS time
        ,unique_id
        ,width
        ,xdid
        ,account AS user_id
        ,ipinfo.admin_code AS ip_admin_code
        ,ipinfo.city AS ip_city
        ,ipinfo.country AS ip_coutry
        ,ipinfo.country_code AS ip_country_code
        ,ipinfo.isp AS ip_isp
        ,ipinfo.latitude AS ip_latitude
        ,ipinfo.longitude AS ip_longitude
        ,ipinfo.province AS ip_province
        ,awaken_item_info

FROM    (
            SELECT  *
                    ,ROW_NUMBER() OVER (PARTITION BY logid ) AS __rnk__
            FROM    tapdb_one_data.ods_torchlight_exposure
            WHERE   dt = '${dt}'
            AND name IN ('exposure_constratin','exposure_store_click','exposure_awaken')
        )
LATERAL VIEW ipinfo_flatten(ip) ipinfo AS country_code,country,province,city,longitude,latitude,isp,admin_code
-- LATERAL VIEW EXPLODE(FROM_JSON(box_id_type_list,'array<string>')) t2 AS exps
WHERE   __rnk__ = 1
;
