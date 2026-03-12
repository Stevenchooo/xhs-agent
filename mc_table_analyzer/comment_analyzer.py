#!/usr/bin/env python3
"""
表用途分析 & Comment 补全建议生成器
基于表名语义 + 字段名推断每张表的业务用途，为缺少 comment 的表生成建议注释
"""
import json
import os
from collections import defaultdict
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), "output")
SCRIPT_DIR = os.path.dirname(__file__)

# ─── 输入文件 ───
DETAIL_FILE = os.path.join(BASE_DIR, "mc_tables_detail.json")
GLOSSARY_FILE = os.path.join(SCRIPT_DIR, "game_glossary.json")
COL_FILES = {
    "tapdb_one_data": os.path.join(BASE_DIR, "columns_tapdb_one_data.json"),
    "tapdb_one_data_asia": os.path.join(BASE_DIR, "columns_tapdb_one_data_asia.json"),
}

# ─── 输出文件 ───
REPORT_FILE = os.path.join(BASE_DIR, "表用途分析与Comment补全建议.md")
JSON_FILE = os.path.join(BASE_DIR, "comment_suggestions.json")

NOW = datetime.now()

# ══════════════════════════════════════════════════════════
#  知识库：表名 / 字段名 → 语义映射
# ══════════════════════════════════════════════════════════

# 分层前缀
LAYERS = {
    "ods": ("ODS", "原始数据层"),
    "dwd": ("DWD", "明细数据层"),
    "dws": ("DWS", "汇总数据层"),
    "dim": ("DIM", "维度表"),
    "ads": ("ADS", "应用数据层"),
    "tmp": ("TMP", "临时表"),
    "stg": ("STG", "暂存层"),
}

# 游戏/业务标识
GAMES = {
    "fp": "Flash Party(派对之星)",
    "t3": "火力苏打",
    "torchlight": "火炬之光",
    "ro": "RO仙境传说",
    "saga": "出发吧麦芬",
    "ssrpg": "铃兰之剑",
    "xdt": "心动小镇",
    "xdtown": "心动小镇",
    "etheria": "伊瑟瑞娅",
    "encrypted": "加密项目",
    "sausage": "香肠派对",
    "sausageman": "香肠派对",
    "taptap": "TapTap平台",
    "tap": "TapTap平台",
    "xdsdk": "XDSDK",
    "themis": "Themis(游戏安全)",
    "tapdb": "TapDB平台",
}

# 区域标识
REGIONS = {
    "os": "海外", "asia": "亚洲", "kr": "韩国", "jp": "日本",
    "us": "美国", "tw": "台湾", "sea": "东南亚", "global": "全球",
    "sg": "新加坡", "cn": "国内",
}

# 时间粒度后缀
GRANULARITY = {
    "di": "日增量", "df": "日全量", "da": "日聚合",
    "hi": "小时增量", "hf": "小时全量",
    "wi": "周增量", "wf": "周全量",
    "mi": "月增量", "mf": "月全量",
    "ri": "实时增量", "rf": "实时全量",
    "fi": "全量增量",
}

# 业务主题关键词
TOPIC_KEYWORDS = {
    # 用户相关
    "user": "用户", "account": "账号", "player": "玩家", "role": "角色",
    "login": "登录", "register": "注册", "regist": "注册",
    "retention": "留存", "active": "活跃", "churn": "流失",
    "new_user": "新用户", "newuser": "新用户",
    # 付费相关
    "pay": "付费", "charge": "充值", "order": "订单", "purchase": "购买",
    "revenue": "收入", "ltv": "LTV", "arpu": "ARPU", "arppu": "ARPPU",
    "refund": "退款", "transaction": "交易",
    # 行为相关
    "event": "事件", "action": "行为", "click": "点击", "view": "浏览",
    "log": "日志", "obt": "OBT", "battle": "战斗", "match": "匹配",
    "level": "等级", "mission": "任务", "quest": "任务",
    "item": "道具", "equip": "装备", "hero": "英雄", "card": "卡牌",
    "guild": "公会", "chat": "聊天", "friend": "好友",
    "gacha": "抽卡", "draw": "抽卡", "summon": "召唤",
    "shop": "商店", "mall": "商城", "exchange": "兑换",
    # 设备/渠道
    "device": "设备", "channel": "渠道", "platform": "平台",
    "install": "安装", "download": "下载", "update": "更新",
    "push": "推送", "notify": "通知", "callback": "回调",
    # 数据运营
    "funnel": "漏斗", "ab_test": "AB测试", "abtest": "AB测试",
    "report": "报表", "statistics": "统计", "summary": "汇总",
    "rank": "排行", "leaderboard": "排行榜",
    "monitor": "监控", "alert": "告警",
    # 基础维度
    "server": "服务器", "zone": "区服", "region": "区域",
    "country": "国家", "city": "城市", "ip": "IP",
    "date": "日期", "time": "时间",
    "config": "配置", "mapping": "映射", "dict": "字典",
    "tag": "标签", "label": "标签", "category": "分类",
    # SDK
    "shiming": "实名认证", "bind": "绑定", "union": "联合登录",
    "translate": "翻译",
}

# 字段名 → 含义（用于推断表用途）
COL_SEMANTICS = {
    "account_id": "账号", "user_id": "用户", "player_id": "玩家", "role_id": "角色",
    "uid": "用户", "open_id": "开放ID", "device_id": "设备",
    "order_id": "订单", "pay_amount": "付费金额", "charge_amount": "充值金额",
    "revenue": "收入", "currency": "货币",
    "login_time": "登录时间", "logout_time": "登出时间",
    "register_time": "注册时间", "create_time": "创建时间",
    "level": "等级", "vip_level": "VIP等级",
    "server_id": "服务器", "zone_id": "区服",
    "channel": "渠道", "platform": "平台",
    "country": "国家", "region": "区域",
    "item_id": "道具", "item_name": "道具名称",
    "event_name": "事件名", "event_type": "事件类型",
    "os": "操作系统", "os_version": "系统版本",
    "app_version": "应用版本", "sdk_version": "SDK版本",
    "ip": "IP地址", "session_id": "会话",
    "dt": "日期分区", "ds": "日期分区", "pt": "分区",
}


# ══════════════════════════════════════════════════════════
#  表名解析器
# ══════════════════════════════════════════════════════════

def parse_table_name(name: str) -> dict:
    """从表名中提取分层、游戏、区域、粒度、主题"""
    parts = name.lower().split("_")
    result = {
        "layer": None, "layer_cn": None,
        "game": None, "game_cn": None,
        "region": None, "region_cn": None,
        "granularity": None, "granularity_cn": None,
        "topics": [],
        "remaining_parts": [],
    }

    idx = 0
    # 1. 分层
    if parts[0] in LAYERS:
        code, cn = LAYERS[parts[0]]
        result["layer"] = code
        result["layer_cn"] = cn
        idx = 1

    # 2. 游戏标识（可能是 1-2 个 token）
    remaining = "_".join(parts[idx:])
    for kw in sorted(GAMES.keys(), key=len, reverse=True):
        if remaining.startswith(kw + "_") or remaining == kw:
            result["game"] = kw
            result["game_cn"] = GAMES[kw]
            # 移动 idx
            kw_parts = kw.split("_")
            idx += len(kw_parts)
            break

    # 3. 区域
    for i, p in enumerate(parts[idx:], idx):
        if p in REGIONS:
            result["region"] = p
            result["region_cn"] = REGIONS[p]
            break

    # 4. 粒度后缀（最后一个 token）
    if parts[-1] in GRANULARITY:
        result["granularity"] = parts[-1]
        result["granularity_cn"] = GRANULARITY[parts[-1]]

    # 5. 主题关键词（用 token 级匹配，避免子串误中）
    rest_parts = set(parts[idx:])
    # 先做完整 token 匹配
    for kw, cn in sorted(TOPIC_KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True):
        kw_tokens = set(kw.split("_"))
        if kw_tokens <= rest_parts and cn not in result["topics"]:
            result["topics"].append(cn)
    # 再做多 token 关键词的连续子串匹配（如 "new_user"）
    rest_str = "_".join(parts[idx:])
    for kw, cn in sorted(TOPIC_KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True):
        if "_" in kw and kw in rest_str and cn not in result["topics"]:
            result["topics"].append(cn)
    result["topics"] = result["topics"][:5]

    result["remaining_parts"] = parts[idx:]
    return result


# ══════════════════════════════════════════════════════════
#  字段分析
# ══════════════════════════════════════════════════════════

def analyze_columns(columns: list) -> dict:
    """分析字段列表，推断业务含义"""
    total = len(columns)
    commented = sum(1 for c in columns if c.get("col_comment", "").strip())
    col_names = [c["col_name"].lower() for c in columns]
    col_types = [c.get("col_type", "") for c in columns]

    # 推断语义标签（精确匹配或前后缀匹配，避免子串误中）
    semantic_tags = []
    for cn in col_names:
        for pattern, label in COL_SEMANTICS.items():
            if label in semantic_tags:
                continue
            # 完全匹配 或 作为前缀/后缀以 _ 分隔出现
            if cn == pattern or f"_{pattern}" in f"_{cn}_":
                semantic_tags.append(label)
    semantic_tags = semantic_tags[:8]

    # 分区字段
    partition_cols = [c["col_name"] for c in columns
                      if c["col_name"].lower() in ("dt", "ds", "pt", "p_date", "partition_date")]

    return {
        "total_columns": total,
        "commented_columns": commented,
        "comment_rate": round(commented / max(1, total) * 100, 1),
        "col_names": [c["col_name"] for c in columns],
        "col_types_summary": _type_summary(col_types),
        "semantic_tags": semantic_tags,
        "partition_cols": partition_cols,
    }


def _type_summary(types: list) -> dict:
    dist = defaultdict(int)
    for t in types:
        base = t.split("(")[0].split("<")[0].upper().strip()
        dist[base] += 1
    return dict(dist)


# ══════════════════════════════════════════════════════════
#  Comment 建议生成
# ══════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════
#  游戏知识库
# ══════════════════════════════════════════════════════════
_GAME_GLOSSARY = None

def load_game_glossary() -> dict:
    global _GAME_GLOSSARY
    if _GAME_GLOSSARY is None:
        try:
            with open(GLOSSARY_FILE, "r", encoding="utf-8") as f:
                _GAME_GLOSSARY = json.load(f)
        except Exception:
            _GAME_GLOSSARY = {}
    return _GAME_GLOSSARY


def get_game_field_comment(game_id: str, field_name: str) -> str:
    """从游戏知识库查找字段的中文释义"""
    glossary = load_game_glossary()
    fn = field_name.lower()

    # 1. 先查游戏专属字段
    game_info = glossary.get("games", {}).get(game_id, {})
    fg = game_info.get("field_glossary", {})
    if fn in fg:
        return fg[fn]

    # 2. 再查通用字段（跳过 _doc 等元数据键）
    common = glossary.get("common_fields", {})
    if fn in common and not fn.startswith("_"):
        return common[fn]

    return ""


def generate_comment_suggestion(table_name: str, parsed: dict, col_analysis: dict,
                                 existing_comment: str) -> str:
    """基于表名解析 + 字段分析 + 游戏知识库，生成建议 comment"""
    if existing_comment and existing_comment.strip():
        return existing_comment.strip()

    parts = []

    # 游戏名
    if parsed.get("game_cn"):
        parts.append(parsed["game_cn"])

    # 区域
    if parsed.get("region_cn"):
        parts.append(parsed["region_cn"])

    # 主题
    topics = parsed.get("topics", [])
    if topics:
        parts.append("_".join(topics[:3]))

    # 如果没有主题，用字段语义
    if not topics and col_analysis.get("semantic_tags"):
        parts.append("_".join(col_analysis["semantic_tags"][:3]))

    # 分层
    if parsed.get("layer_cn"):
        parts.append(f"({parsed['layer_cn']})")

    # 粒度
    if parsed.get("granularity_cn"):
        parts.append(f"[{parsed['granularity_cn']}]")

    if parts:
        return " ".join(parts)

    # 兜底：用剩余表名部分
    remaining = "_".join(parsed.get("remaining_parts", []))
    return f"({remaining})" if remaining else table_name


# ══════════════════════════════════════════════════════════
#  主流程
# ══════════════════════════════════════════════════════════

def load_table_comments(space_name: str) -> dict:
    """从 detail 文件加载表级 comment"""
    try:
        with open(DETAIL_FILE, "r") as f:
            detail = json.load(f)
        if space_name in detail:
            return {t["table_name"]: t.get("comment", "") for t in detail[space_name]["tables"]}
    except Exception:
        pass
    return {}


def run():
    report_lines = []
    all_suggestions = {}

    w = report_lines.append
    w("# 表用途分析与 Comment 补全建议\n")
    w(f"> 生成时间: {NOW.strftime('%Y-%m-%d %H:%M:%S')}\n")
    w("---\n")

    for space_name, col_file in COL_FILES.items():
        print(f"📊 加载 {space_name} ...")

        # 加载列信息
        with open(col_file, "r", encoding="utf-8") as f:
            columns_data = json.load(f)

        # 加载表级 comment
        table_comments = load_table_comments(space_name)

        tables_analysis = []
        total = len(columns_data)
        need_comment = 0
        total_cols = 0
        cols_with_comment = 0

        for tname, tcols in columns_data.items():
            existing_comment = table_comments.get(tname, "")
            parsed = parse_table_name(tname)
            col_analysis = analyze_columns(tcols)

            total_cols += col_analysis["total_columns"]
            cols_with_comment += col_analysis["commented_columns"]

            suggestion = generate_comment_suggestion(tname, parsed, col_analysis, existing_comment)
            has_comment = bool(existing_comment and existing_comment.strip())
            if not has_comment:
                need_comment += 1

            tables_analysis.append({
                "table_name": tname,
                "existing_comment": existing_comment,
                "has_comment": has_comment,
                "suggested_comment": suggestion,
                "layer": parsed.get("layer", ""),
                "layer_cn": parsed.get("layer_cn", ""),
                "game": parsed.get("game", ""),
                "game_cn": parsed.get("game_cn", ""),
                "region_cn": parsed.get("region_cn", ""),
                "granularity_cn": parsed.get("granularity_cn", ""),
                "topics": parsed.get("topics", []),
                "col_count": col_analysis["total_columns"],
                "col_commented": col_analysis["commented_columns"],
                "col_comment_rate": col_analysis["comment_rate"],
                "col_semantic_tags": col_analysis["semantic_tags"],
                "col_names": col_analysis["col_names"],
                "partition_cols": col_analysis["partition_cols"],
            })

        print(f"   ✅ {total} 张表, 需补 comment: {need_comment}, "
              f"列注释覆盖: {cols_with_comment}/{total_cols} ({cols_with_comment/max(1,total_cols)*100:.1f}%)")

        all_suggestions[space_name] = tables_analysis

        # ─── 写入报告 ───
        region_label = "国内 cn-beijing" if "asia" not in space_name else "海外 ap-southeast-1"
        w(f"## {space_name} ({region_label})\n")

        # 概览
        w("### 注释覆盖率\n")
        w("| 指标 | 数值 |")
        w("|---|---:|")
        w(f"| 表总数 | {total:,} |")
        w(f"| 已有表注释 | {total - need_comment:,} ({(total-need_comment)/max(1,total)*100:.1f}%) |")
        w(f"| **需补表注释** | **{need_comment:,}** ({need_comment/max(1,total)*100:.1f}%) |")
        w(f"| 字段总数 | {total_cols:,} |")
        w(f"| 已有字段注释 | {cols_with_comment:,} ({cols_with_comment/max(1,total_cols)*100:.1f}%) |")
        w(f"| 需补字段注释 | {total_cols - cols_with_comment:,} ({(total_cols-cols_with_comment)/max(1,total_cols)*100:.1f}%) |")
        w("")

        # 按游戏分组统计注释缺失
        game_stats = defaultdict(lambda: {"total": 0, "no_comment": 0, "no_col_comment_tables": 0})
        for ta in tables_analysis:
            g = ta["game_cn"] or "其他/通用"
            game_stats[g]["total"] += 1
            if not ta["has_comment"]:
                game_stats[g]["no_comment"] += 1
            if ta["col_comment_rate"] == 0:
                game_stats[g]["no_col_comment_tables"] += 1

        w("### 各游戏/业务线注释缺失分布\n")
        w("| 游戏/业务 | 表总数 | 缺表注释 | 列注释全空表 |")
        w("|---|---:|---:|---:|")
        for g, s in sorted(game_stats.items(), key=lambda x: x[1]["no_comment"], reverse=True):
            w(f"| {g} | {s['total']:,} | {s['no_comment']:,} | {s['no_col_comment_tables']:,} |")
        w("")

        # 按分层分组
        layer_stats = defaultdict(lambda: {"total": 0, "no_comment": 0})
        for ta in tables_analysis:
            l = ta["layer_cn"] or "其他"
            layer_stats[l]["total"] += 1
            if not ta["has_comment"]:
                layer_stats[l]["no_comment"] += 1

        w("### 各分层注释缺失分布\n")
        w("| 分层 | 表总数 | 缺表注释 | 缺失率 |")
        w("|---|---:|---:|---:|")
        for l, s in sorted(layer_stats.items(), key=lambda x: x[1]["no_comment"], reverse=True):
            rate = s["no_comment"] / max(1, s["total"]) * 100
            w(f"| {l} | {s['total']:,} | {s['no_comment']:,} | {rate:.1f}% |")
        w("")

        # 需补 comment 的表清单（按游戏分组输出）
        w("### Comment 补全建议清单\n")
        w("> 以下按游戏/业务线分组，列出需要补全 comment 的表及建议注释\n")

        no_comment_tables = [ta for ta in tables_analysis if not ta["has_comment"]]
        grouped = defaultdict(list)
        for ta in no_comment_tables:
            g = ta["game_cn"] or "其他/通用"
            grouped[g].append(ta)

        for game, items in sorted(grouped.items(), key=lambda x: len(x[1]), reverse=True):
            w(f"#### {game} ({len(items)} 张表)\n")
            w("| 表名 | 建议注释 | 字段数 | 字段注释率 | 语义标签 |")
            w("|---|---|---:|---:|---|")
            for ta in sorted(items, key=lambda x: x["table_name"]):
                tags = ", ".join(ta["col_semantic_tags"][:4]) if ta["col_semantic_tags"] else "-"
                w(f"| {ta['table_name']} | {ta['suggested_comment']} "
                  f"| {ta['col_count']} | {ta['col_comment_rate']}% | {tags} |")
            w("")

    # 总结
    w("## 补全优先级建议\n")
    w("1. **高优先级**: ADS/DWS 层的表（直接面向应用和报表）")
    w("2. **中优先级**: DWD/DIM 层的表（数据加工核心层）")
    w("3. **低优先级**: ODS 层的表（原始数据，一般与源表一一对应）")
    w("4. **可跳过**: TMP 临时表（生命周期短，不需要长期维护注释）")
    w("")
    w("---\n")
    w(f"*由 comment_analyzer 自动生成 · {NOW.strftime('%Y-%m-%d %H:%M:%S')}*\n")

    # 保存报告
    report_text = "\n".join(report_lines)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\n📄 报告已保存: {REPORT_FILE}")

    # 保存 JSON（含游戏知识库增强的字段注释建议）
    json_out = {}
    for space, items in all_suggestions.items():
        enriched_tables = []
        for i in items:
            if i["has_comment"]:
                continue
            game_id = i.get("game", "")
            # 用知识库为每个字段生成注释建议（无游戏前缀也查 common_fields）
            col_suggestions = {}
            if i.get("col_names"):
                for cn in i["col_names"]:
                    gl_comment = get_game_field_comment(game_id, cn)
                    if gl_comment:
                        col_suggestions[cn] = gl_comment
            enriched_tables.append({
                "table_name": i["table_name"],
                "suggested_comment": i["suggested_comment"],
                "layer": i["layer"],
                "game": game_id,
                "game_cn": i["game_cn"],
                "col_count": i["col_count"],
                "col_comment_rate": i["col_comment_rate"],
                "col_semantic_tags": i["col_semantic_tags"],
                "col_comment_suggestions": col_suggestions,
            })
        json_out[space] = {
            "total": len(items),
            "need_comment": sum(1 for i in items if not i["has_comment"]),
            "tables": enriched_tables,
        }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_out, f, ensure_ascii=False, indent=2)
    print(f"📊 JSON 数据: {JSON_FILE}")

    # 打印摘要
    for space, items in all_suggestions.items():
        nc = sum(1 for i in items if not i["has_comment"])
        print(f"\n  {space}: {len(items)} 张表, {nc} 张需补 comment")


if __name__ == "__main__":
    run()
