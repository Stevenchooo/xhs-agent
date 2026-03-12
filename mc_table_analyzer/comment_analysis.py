#!/usr/bin/env python3
"""
分析每张表的用途和字段，为补全 comment 做准备
根据表名模式 + 字段名模式 → 推断表用途 → 生成建议 comment
输出可直接执行的 ALTER TABLE 语句
"""
import os
import json
import re
from collections import defaultdict

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
DETAIL_FILE = os.path.join(OUTPUT_DIR, "mc_tables_detail.json")

# ─── 分层含义 ───
LAYER_MAP = {
    "ods": "原始数据",
    "dwd": "明细数据",
    "dws": "汇总数据",
    "dim": "维度表",
    "ads": "应用数据",
    "tmp": "临时表",
    "stg": "暂存数据",
}

# ─── 游戏/业务关键词 ───
GAME_MAP = {
    "fp": "Flash Party(闪派对)",
    "t3": "火炬之光:无限(T3)",
    "torchlight": "火炬之光",
    "ro": "RO仙境传说",
    "saga": "Saga传说",
    "ssrpg": "SSRPG",
    "xdt": "心动Town",
    "etheria": "以太芝境",
    "xdsdk": "XDSDK",
    "taptap": "TapTap",
    "tap": "TapTap",
    "themis": "Themis游戏安全",
    "sausage": "香肠派对",
    "encrypted": "加密",
    "ad": "广告",
}

# ─── 区域后缀 ───
REGION_MAP = {
    "os": "海外",
    "kr": "韩国",
    "jp": "日本",
    "tw": "台湾",
    "us": "美国",
    "sea": "东南亚",
    "global": "全球",
    "asia": "亚洲",
}

# ─── 时间后缀 ───
TIME_SUFFIX = {
    "di": "日增量",
    "df": "日全量快照",
    "da": "日累计",
    "wi": "周增量",
    "wf": "周全量快照",
    "mi": "月增量",
    "mf": "月全量快照",
    "ri": "全量同步",
    "hi": "小时增量",
}

# ─── 实体关键词 ───
ENTITY_KEYWORDS = {
    "user": "用户",
    "account": "账号",
    "role": "角色",
    "player": "玩家",
    "login": "登录",
    "logout": "登出",
    "register": "注册",
    "charge": "充值",
    "pay": "支付",
    "order": "订单",
    "item": "道具",
    "equip": "装备",
    "hero": "英雄",
    "career": "职业",
    "level": "等级",
    "battle": "战斗",
    "match": "匹配",
    "quest": "任务",
    "mission": "任务",
    "dungeon": "副本",
    "guild": "公会",
    "friend": "好友",
    "chat": "聊天",
    "mail": "邮件",
    "shop": "商店",
    "event": "事件",
    "action": "行为",
    "activity": "活动",
    "sign": "签到",
    "gacha": "抽卡",
    "summon": "召唤",
    "draw": "抽卡",
    "rank": "排行",
    "arena": "竞技场",
    "pvp": "PVP对战",
    "pve": "PVE",
    "skill": "技能",
    "talent": "天赋",
    "task": "任务",
    "achievement": "成就",
    "retention": "留存",
    "ltv": "生命周期价值",
    "dau": "日活",
    "mau": "月活",
    "funnel": "漏斗",
    "device": "设备",
    "server": "服务器",
    "channel": "渠道",
    "region": "区服",
    "config": "配置",
    "log": "日志",
    "obt": "OBT原始数据",
    "cat": "CAT数据",
    "mapping": "映射关系",
    "statistics": "统计",
    "summary": "汇总",
    "detail": "明细",
    "snapshot": "快照",
    "archive": "归档",
    "backup": "备份",
    "temp": "临时",
    "test": "测试",
    "die": "死亡",
    "boss": "Boss",
    "monster": "怪物",
    "npc": "NPC",
    "trade": "交易",
    "auction": "拍卖",
    "market": "市场",
    "inventory": "背包",
    "pet": "宠物",
    "mount": "坐骑",
    "relic": "遗物",
    "grow": "成长",
    "upgrade": "升级",
    "enhance": "强化",
    "refine": "精炼",
    "craft": "制作",
    "produce": "生产",
    "resource": "资源",
    "currency": "货币",
    "diamond": "钻石",
    "gold": "金币",
    "token": "代币",
    "coupon": "优惠券",
    "promotion": "推广",
    "click": "点击",
    "view": "浏览",
    "impression": "曝光",
    "conversion": "转化",
    "install": "安装",
    "download": "下载",
    "update": "更新",
    "version": "版本",
    "crash": "崩溃",
    "error": "错误",
    "performance": "性能",
    "risk": "风控",
    "ban": "封禁",
    "cheat": "作弊",
    "review": "评测",
    "rating": "评分",
    "feedback": "反馈",
    "survey": "调查",
    "notification": "通知",
    "push": "推送",
    "bind": "绑定",
    "shiming": "实名",
    "mobiles": "手机号",
    "compensation": "补偿",
    "announce": "公告",
}


def infer_comment(table_name: str, columns: list = None) -> str:
    """根据表名和字段推断表用途，生成建议 comment"""
    parts = table_name.lower().split("_")

    # 1. 分层
    layer = ""
    rest_parts = parts
    if parts[0] in LAYER_MAP:
        layer = LAYER_MAP[parts[0]]
        rest_parts = parts[1:]

    # 2. 游戏/业务
    game = ""
    consumed = 0
    for i in range(min(3, len(rest_parts))):
        candidate = "_".join(rest_parts[:i + 1])
        for kw, name in GAME_MAP.items():
            if candidate == kw or candidate.startswith(kw + "_"):
                game = name
                consumed = i + 1 if candidate == kw else 1
                break
        if game:
            break

    rest_parts = rest_parts[consumed:]

    # 3. 区域
    region = ""
    if rest_parts and rest_parts[0] in REGION_MAP:
        region = REGION_MAP[rest_parts[0]]
        rest_parts = rest_parts[1:]
    # 检查倒数的区域后缀
    if not region and len(rest_parts) >= 2 and rest_parts[-2] in REGION_MAP:
        pass  # 不从末尾取，避免误判

    # 4. 时间粒度后缀
    time_suffix = ""
    if rest_parts and rest_parts[-1] in TIME_SUFFIX:
        time_suffix = TIME_SUFFIX[rest_parts[-1]]
        rest_parts = rest_parts[:-1]

    # 5. 实体关键词
    entity_words = []
    remaining = "_".join(rest_parts)
    for kw, cn in ENTITY_KEYWORDS.items():
        if kw in remaining.split("_"):
            entity_words.append(cn)

    # 6. 组装 comment
    comment_parts = []
    if game:
        comment_parts.append(game)
    if region:
        comment_parts.append(region)
    if entity_words:
        comment_parts.append("·".join(entity_words[:3]))
    if layer:
        comment_parts.append(f"({layer})")
    if time_suffix:
        comment_parts.append(f"[{time_suffix}]")

    # 如果什么都没推断出来，用原名
    if not comment_parts:
        return f"[待补充] {table_name}"

    return " ".join(comment_parts)


def analyze_columns(columns: list) -> dict:
    """分析字段列表，提取关键信息"""
    col_count = len(columns)
    has_comment = sum(1 for c in columns if c.get("col_comment", "").strip())
    comment_rate = has_comment / max(1, col_count) * 100

    # 分区字段
    partition_cols = [c for c in columns if c.get("col_type", "").upper() == "STRING"
                      and c.get("col_name", "") in ("dt", "ds", "pt", "region", "game_id")]

    # 关键字段
    id_cols = [c["col_name"] for c in columns if "id" in c.get("col_name", "").lower()]
    time_cols = [c["col_name"] for c in columns
                 if any(t in c.get("col_name", "").lower() for t in ("time", "date", "day", "dt"))]

    return {
        "col_count": col_count,
        "col_with_comment": has_comment,
        "col_comment_rate": round(comment_rate, 1),
        "id_columns": id_cols[:5],
        "time_columns": time_cols[:5],
        "column_names": [c["col_name"] for c in columns],
        "column_types": [c["col_type"] for c in columns],
    }


def main():
    # 加载表元信息
    with open(DETAIL_FILE, "r", encoding="utf-8") as f:
        detail_data = json.load(f)

    for space_name in ["tapdb_one_data", "tapdb_one_data_asia"]:
        print(f"\n{'=' * 70}")
        print(f"  分析空间: {space_name}")
        print(f"{'=' * 70}")

        # 加载字段信息
        col_file = os.path.join(OUTPUT_DIR, f"columns_{space_name}.json")
        if not os.path.exists(col_file):
            print(f"  ⚠️  字段文件不存在: {col_file}")
            print(f"  请先运行 fetch_columns.py 拉取字段数据")
            continue

        with open(col_file, "r", encoding="utf-8") as f:
            columns_data = json.load(f)

        # 加载已有表信息
        space_info = detail_data.get(space_name, {})
        tables_list = space_info.get("tables", [])
        existing_comments = {t["table_name"]: t.get("comment", "") for t in tables_list}

        print(f"  📊 总表数: {len(tables_list):,}")
        print(f"  📊 有字段信息的表: {len(columns_data):,}")

        no_comment_tables = [t for t in tables_list if not t.get("comment", "").strip()]
        print(f"  📊 无注释的表: {len(no_comment_tables):,}")

        # 逐表分析
        results = []
        alter_statements = []

        for t in tables_list:
            tname = t["table_name"]
            existing_comment = t.get("comment", "").strip()
            cols = columns_data.get(tname, [])
            col_analysis = analyze_columns(cols) if cols else None

            suggested_comment = infer_comment(tname, cols)

            entry = {
                "table_name": tname,
                "existing_comment": existing_comment,
                "suggested_comment": suggested_comment,
                "needs_comment": not existing_comment,
                "table_type": t.get("type", ""),
                "owner": t.get("owner", "").split(":")[-1],
                "size": t.get("size", 0),
                "life_cycle": t.get("life_cycle", 0),
                "last_modified": t.get("last_modified_time", ""),
            }

            if col_analysis:
                entry.update({
                    "col_count": col_analysis["col_count"],
                    "col_comment_rate": col_analysis["col_comment_rate"],
                    "id_columns": col_analysis["id_columns"],
                    "time_columns": col_analysis["time_columns"],
                    "all_columns": col_analysis["column_names"],
                    "all_column_types": col_analysis["column_types"],
                })

            results.append(entry)

            # 生成 ALTER TABLE 语句 (仅对无注释的表)
            if not existing_comment:
                safe_comment = suggested_comment.replace("'", "\\'")
                alter_statements.append(
                    f"ALTER TABLE {tname} SET COMMENT '{safe_comment}';"
                )

        # ── 保存分析结果 JSON ──
        analysis_file = os.path.join(OUTPUT_DIR, f"comment_analysis_{space_name}.json")
        with open(analysis_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        print(f"  💾 分析结果: {analysis_file}")

        # ── 保存 ALTER TABLE SQL ──
        sql_file = os.path.join(OUTPUT_DIR, f"alter_comments_{space_name}.sql")
        with open(sql_file, "w", encoding="utf-8") as f:
            f.write(f"-- {space_name} 表注释补全 SQL\n")
            f.write(f"-- 共 {len(alter_statements)} 张表需要补全注释\n")
            f.write(f"-- 生成时间: {__import__('datetime').datetime.now()}\n")
            f.write(f"-- ⚠️ 请人工 review 后再执行\n\n")
            f.write("\n".join(alter_statements))
        print(f"  💾 ALTER SQL: {sql_file}")

        # ── 生成报告 ──
        report_file = os.path.join(OUTPUT_DIR, f"comment_report_{space_name}.md")
        generate_space_report(space_name, results, columns_data, report_file)
        print(f"  💾 分析报告: {report_file}")


def generate_space_report(space_name: str, results: list, columns_data: dict, report_file: str):
    """生成单空间的表字段分析报告"""
    lines = []
    w = lines.append

    w(f"# {space_name} 表用途与字段分析报告\n")
    w(f"> 为补全 table comment 做准备\n")

    total = len(results)
    needs_comment = sum(1 for r in results if r["needs_comment"])
    has_cols = sum(1 for r in results if r.get("col_count", 0) > 0)

    w("## 概览\n")
    w(f"| 指标 | 数值 |")
    w(f"|---|---|")
    w(f"| 总表数 | {total:,} |")
    w(f"| 需补注释 | **{needs_comment:,}** ({needs_comment / max(1, total) * 100:.1f}%) |")
    w(f"| 已有注释 | {total - needs_comment:,} |")
    w(f"| 有字段信息 | {has_cols:,} |")
    w("")

    # ── 按游戏/业务分组列出需补注释的表 ──
    w("## 需补注释的表（按推断业务分组）\n")

    # 按建议 comment 的业务前缀分组
    game_groups = defaultdict(list)
    for r in results:
        if not r["needs_comment"]:
            continue
        comment = r["suggested_comment"]
        # 取第一个关键词作为分组
        game = comment.split(" ")[0] if comment else "未知"
        game_groups[game].append(r)

    for game, tables in sorted(game_groups.items(), key=lambda x: len(x[1]), reverse=True):
        w(f"### {game} ({len(tables)} 张表)\n")
        w("| 表名 | 建议注释 | 字段数 | 字段注释率 | 存储 | Owner |")
        w("|---|---|---:|---:|---:|---|")

        for r in sorted(tables, key=lambda x: x.get("col_count", 0), reverse=True)[:50]:
            tname = r["table_name"]
            sug = r["suggested_comment"]
            cc = r.get("col_count", "-")
            ccr = f"{r.get('col_comment_rate', 0):.0f}%" if r.get("col_comment_rate") is not None else "-"
            size = r.get("size", 0)
            size_str = format_size(size)
            owner = r.get("owner", "")
            w(f"| {tname} | {sug} | {cc} | {ccr} | {size_str} | {owner} |")

        if len(tables) > 50:
            w(f"\n> *... 省略 {len(tables) - 50} 张表*\n")
        w("")

    # ── 字段信息采样：按分层展示典型表结构 ──
    w("## 典型表字段结构示例\n")
    w("以下展示各分层的代表性表的字段信息：\n")

    layers = ["ods", "dwd", "dws", "dim", "ads"]
    shown = set()
    for layer in layers:
        # 找一个有字段信息且有注释的代表表
        candidates = [r for r in results
                      if r["table_name"].lower().startswith(layer + "_")
                      and r.get("col_count", 0) >= 5
                      and r["table_name"] not in shown]
        if not candidates:
            continue
        # 优先选有注释的
        candidates.sort(key=lambda x: (bool(x.get("existing_comment")), x.get("col_count", 0)), reverse=True)
        sample = candidates[0]
        shown.add(sample["table_name"])

        tname = sample["table_name"]
        comment = sample.get("existing_comment") or sample.get("suggested_comment", "")
        cols = columns_data.get(tname, [])

        w(f"### {layer.upper()} 层示例: `{tname}`")
        w(f"- 注释: {comment}")
        w(f"- 字段数: {len(cols)}\n")
        w("| # | 字段名 | 类型 | 注释 |")
        w("|---:|---|---|---|")
        for i, c in enumerate(cols[:30], 1):
            w(f"| {i} | {c['col_name']} | {c['col_type']} | {c.get('col_comment', '')} |")
        if len(cols) > 30:
            w(f"| ... | *共 {len(cols)} 个字段* | | |")
        w("")

    w("---\n")
    w(f"*由 comment_analysis.py 自动生成*\n")

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def format_size(size_bytes):
    if not size_bytes or size_bytes < 0:
        return "-"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / 1024 ** 2:.1f} MB"
    elif size_bytes < 1024 ** 4:
        return f"{size_bytes / 1024 ** 3:.2f} GB"
    else:
        return f"{size_bytes / 1024 ** 4:.2f} TB"


if __name__ == "__main__":
    main()
