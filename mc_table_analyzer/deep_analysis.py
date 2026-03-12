#!/usr/bin/env python3
"""
深度分析 tapdb_one_data & tapdb_one_data_asia 两大空间的全部表信息
生成完整分析报告文档
"""
import json
import os
from collections import defaultdict
from datetime import datetime

DETAIL_FILE = os.path.join(os.path.dirname(__file__), "output", "mc_tables_detail.json")
REPORT_FILE = os.path.join(os.path.dirname(__file__), "output", "全空间表分析报告.md")

TARGET_SPACES = ["tapdb_one_data", "tapdb_one_data_asia"]

# ─── 分层 ───
LAYER_PREFIXES = {
    "ods": "ODS (原始层)",
    "dwd": "DWD (明细层)",
    "dws": "DWS (汇总层)",
    "dim": "DIM (维度层)",
    "ads": "ADS (应用层)",
    "tmp": "TMP (临时表)",
    "stg": "STG (暂存层)",
}

# ─── 游戏/业务关键词 → 归属项目（与 game_glossary.json 保持一致）───
GAME_KEYWORDS = {
    "fp": "Flash Party(派对之星)",
    "t3": "火力苏打",
    "torchlight": "火炬之光·无限",
    "ro": "RO仙境传说",
    "saga": "出发吧麦芬",
    "ssrpg": "铃兰之剑",
    "xdt": "心动小镇",
    "xdtown": "心动小镇",
    "etheria": "伊瑟瑞娅",
    "encrypted": "加密项目",
    "sausage": "香肠派对",
    "sausageman": "香肠派对",
    "xdsdk": "XDSDK",
    "taptap": "TapTap平台",
    "tap": "TapTap平台",
    "tapdb": "TapDB平台",
    "themis": "Themis(游戏安全)",
    "qs": "浅水工作室",
}

NOW = datetime.now()


def load_data():
    with open(DETAIL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if k in TARGET_SPACES}


def classify_layer(name: str) -> str:
    nl = name.lower()
    for prefix, label in LAYER_PREFIXES.items():
        if nl.startswith(prefix + "_"):
            return label
    return "其他"


def guess_game(name: str) -> str:
    """根据表名猜测所属游戏/业务"""
    nl = name.lower()
    # 去掉分层前缀
    parts = nl.split("_")
    if parts[0] in LAYER_PREFIXES:
        parts = parts[1:]
    remaining = "_".join(parts)

    # 长关键词优先匹配，避免短词误中
    for kw in sorted(GAME_KEYWORDS.keys(), key=len, reverse=True):
        if remaining.startswith(kw + "_") or remaining == kw:
            return GAME_KEYWORDS[kw]
    return "其他/通用"


def parse_time(ts: str):
    if not ts:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return None


def format_size(size_bytes):
    if size_bytes is None or size_bytes < 0:
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


def analyze_space(space_name: str, tables: list) -> dict:
    """多维度分析"""
    result = {
        "space_name": space_name,
        "total_tables": len(tables),
        "total_size": 0,
        "managed_tables": 0,
        "virtual_views": 0,
        "external_tables": 0,
        "layer_dist": defaultdict(int),
        "game_dist": defaultdict(int),
        "owner_dist": defaultdict(int),
        "lifecycle_dist": defaultdict(int),
        "year_created_dist": defaultdict(int),
        "active_30d": 0,
        "active_90d": 0,
        "active_180d": 0,
        "active_365d": 0,
        "stale_over_1y": 0,
        "no_lifecycle": 0,
        "top_large_tables": [],
        "tables_no_comment": 0,
    }

    size_list = []

    for t in tables:
        tname = t.get("table_name", "")
        ttype = t.get("type", "")
        size = t.get("size", 0) or 0
        if size < 0:
            size = 0
        lc = t.get("life_cycle", 0) or 0
        comment = t.get("comment", "")
        owner = t.get("owner", "未知")
        ct = t.get("creation_time", "")
        mt = t.get("last_modified_time", "")

        result["total_size"] += size

        # 表类型
        if "VIEW" in ttype.upper():
            result["virtual_views"] += 1
        elif "EXTERNAL" in ttype.upper():
            result["external_tables"] += 1
        else:
            result["managed_tables"] += 1

        # 分层
        result["layer_dist"][classify_layer(tname)] += 1

        # 游戏/业务
        result["game_dist"][guess_game(tname)] += 1

        # Owner（简化显示）
        owner_short = owner.split(":")[-1] if ":" in owner else owner
        result["owner_dist"][owner_short] += 1

        # 生命周期
        if lc <= 0:
            result["no_lifecycle"] += 1
            result["lifecycle_dist"]["未设置"] += 1
        elif lc <= 30:
            result["lifecycle_dist"]["≤30天"] += 1
        elif lc <= 90:
            result["lifecycle_dist"]["31-90天"] += 1
        elif lc <= 180:
            result["lifecycle_dist"]["91-180天"] += 1
        elif lc <= 365:
            result["lifecycle_dist"]["181-365天"] += 1
        else:
            result["lifecycle_dist"][">365天"] += 1

        # 创建年份
        ct_dt = parse_time(ct)
        if ct_dt:
            result["year_created_dist"][ct_dt.year] += 1

        # 活跃度（按最后修改时间）
        mt_dt = parse_time(mt)
        if mt_dt:
            delta = (NOW - mt_dt).days
            if delta <= 30:
                result["active_30d"] += 1
            if delta <= 90:
                result["active_90d"] += 1
            if delta <= 180:
                result["active_180d"] += 1
            if delta <= 365:
                result["active_365d"] += 1
            if delta > 365:
                result["stale_over_1y"] += 1

        # 注释
        if not comment or not comment.strip():
            result["tables_no_comment"] += 1

        # 存储记录
        size_list.append((tname, size, ttype, owner_short, comment, lc, ct, mt))

    # Top 大表
    size_list.sort(key=lambda x: x[1], reverse=True)
    result["top_large_tables"] = size_list[:30]

    # 转 dict
    result["layer_dist"] = dict(result["layer_dist"])
    result["game_dist"] = dict(result["game_dist"])
    result["owner_dist"] = dict(result["owner_dist"])
    result["lifecycle_dist"] = dict(result["lifecycle_dist"])
    result["year_created_dist"] = dict(result["year_created_dist"])

    return result


def generate_report(analyses: dict) -> str:
    """生成 Markdown 格式报告"""
    lines = []
    w = lines.append

    w("# MaxCompute 核心空间表分析报告\n")
    w(f"> 生成时间: {NOW.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # ── 概览 ──
    total_t = sum(a["total_tables"] for a in analyses.values())
    total_s = sum(a["total_size"] for a in analyses.values())

    w("## 一、总体概览\n")
    w("| 指标 | 数值 |")
    w("|---|---|")
    w(f"| 分析空间数 | {len(analyses)} |")
    w(f"| 表总数 | **{total_t:,}** |")
    w(f"| 总存储 | **{format_size(total_s)}** |")
    w("")

    w("| 空间 | 区域 | 表数量 | 存储 | 托管表 | 视图 | 外部表 |")
    w("|---|---|---:|---:|---:|---:|---:|")
    for sname, a in analyses.items():
        region = "cn-beijing" if "asia" not in sname else "ap-southeast-1"
        w(f"| {sname} | {region} | {a['total_tables']:,} | {format_size(a['total_size'])} "
          f"| {a['managed_tables']:,} | {a['virtual_views']:,} | {a['external_tables']:,} |")
    w("")

    # ── 逐空间详细分析 ──
    for sname, a in analyses.items():
        region_label = "国内 (cn-beijing)" if "asia" not in sname else "海外 (ap-southeast-1)"
        w(f"## 二、{sname} ({region_label})\n")

        # 2.1 分层分布
        w(f"### 2.1 表分层分布（共 {a['total_tables']:,} 张表）\n")
        w("| 分层 | 数量 | 占比 | 柱状 |")
        w("|---|---:|---:|---|")
        for layer, cnt in sorted(a["layer_dist"].items(), key=lambda x: x[1], reverse=True):
            pct = cnt / max(1, a["total_tables"]) * 100
            bar = "█" * int(pct / 2)
            w(f"| {layer} | {cnt:,} | {pct:.1f}% | {bar} |")
        w("")

        # 2.2 游戏/业务分布
        w("### 2.2 游戏/业务线分布\n")
        w("| 游戏/业务 | 表数量 | 占比 |")
        w("|---|---:|---:|")
        for game, cnt in sorted(a["game_dist"].items(), key=lambda x: x[1], reverse=True):
            pct = cnt / max(1, a["total_tables"]) * 100
            w(f"| {game} | {cnt:,} | {pct:.1f}% |")
        w("")

        # 2.3 Owner 分布
        w("### 2.3 表 Owner 分布（Top 15）\n")
        w("| Owner | 表数量 | 占比 |")
        w("|---|---:|---:|")
        sorted_owners = sorted(a["owner_dist"].items(), key=lambda x: x[1], reverse=True)[:15]
        for owner, cnt in sorted_owners:
            pct = cnt / max(1, a["total_tables"]) * 100
            w(f"| {owner} | {cnt:,} | {pct:.1f}% |")
        if len(a["owner_dist"]) > 15:
            rest = sum(c for _, c in sorted(a["owner_dist"].items(), key=lambda x: x[1], reverse=True)[15:])
            w(f"| *其他 ({len(a['owner_dist']) - 15} 人)* | {rest:,} | {rest / max(1, a['total_tables']) * 100:.1f}% |")
        w("")

        # 2.4 生命周期
        w("### 2.4 生命周期设置\n")
        w("| 生命周期 | 表数量 | 占比 |")
        w("|---|---:|---:|")
        lc_order = ["未设置", "≤30天", "31-90天", "91-180天", "181-365天", ">365天"]
        for lc in lc_order:
            cnt = a["lifecycle_dist"].get(lc, 0)
            pct = cnt / max(1, a["total_tables"]) * 100
            w(f"| {lc} | {cnt:,} | {pct:.1f}% |")
        w("")
        w(f"> ⚠️ **未设置生命周期的表: {a['no_lifecycle']:,} 张** "
          f"({a['no_lifecycle'] / max(1, a['total_tables']) * 100:.1f}%)，建议梳理后设置合理的生命周期以节省存储成本。\n")

        # 2.5 活跃度
        w("### 2.5 表活跃度分析\n")
        w("| 时间窗口 | 活跃表数 | 占比 |")
        w("|---|---:|---:|")
        w(f"| 最近 30 天有更新 | {a['active_30d']:,} | {a['active_30d'] / max(1, a['total_tables']) * 100:.1f}% |")
        w(f"| 最近 90 天有更新 | {a['active_90d']:,} | {a['active_90d'] / max(1, a['total_tables']) * 100:.1f}% |")
        w(f"| 最近 180 天有更新 | {a['active_180d']:,} | {a['active_180d'] / max(1, a['total_tables']) * 100:.1f}% |")
        w(f"| 最近 365 天有更新 | {a['active_365d']:,} | {a['active_365d'] / max(1, a['total_tables']) * 100:.1f}% |")
        w(f"| **超过 1 年未更新** | **{a['stale_over_1y']:,}** | **{a['stale_over_1y'] / max(1, a['total_tables']) * 100:.1f}%** |")
        w("")

        # 2.6 建表年份
        w("### 2.6 建表年份分布\n")
        w("| 年份 | 新建表数 | 占比 |")
        w("|---|---:|---:|")
        for year in sorted(a["year_created_dist"].keys()):
            cnt = a["year_created_dist"][year]
            pct = cnt / max(1, a["total_tables"]) * 100
            w(f"| {year} | {cnt:,} | {pct:.1f}% |")
        w("")

        # 2.7 表注释
        w("### 2.7 表注释覆盖率\n")
        commented = a["total_tables"] - a["tables_no_comment"]
        w(f"- 有注释的表: **{commented:,}** ({commented / max(1, a['total_tables']) * 100:.1f}%)")
        w(f"- 无注释的表: **{a['tables_no_comment']:,}** ({a['tables_no_comment'] / max(1, a['total_tables']) * 100:.1f}%)")
        w("")

        # 2.8 Top 大表
        w("### 2.8 存储 Top 30 大表\n")
        w("| # | 表名 | 存储 | 类型 | Owner | 生命周期 | 最后更新 |")
        w("|---:|---|---:|---|---|---:|---|")
        for i, (tname, size, ttype, owner, comment, lc, ct, mt) in enumerate(a["top_large_tables"], 1):
            ttype_short = "VIEW" if "VIEW" in ttype.upper() else "TABLE"
            lc_str = f"{lc}天" if lc > 0 else "未设置"
            w(f"| {i} | {tname} | {format_size(size)} | {ttype_short} | {owner} | {lc_str} | {mt[:10] if mt else '-'} |")
        w("")

    # ── 对比分析 ──
    w("## 三、国内 vs 海外对比\n")
    keys_cn = "tapdb_one_data"
    keys_os = "tapdb_one_data_asia"
    cn = analyses.get(keys_cn, {})
    os_a = analyses.get(keys_os, {})

    w("| 维度 | 国内 (tapdb_one_data) | 海外 (tapdb_one_data_asia) |")
    w("|---|---:|---:|")
    w(f"| 表总数 | {cn.get('total_tables', 0):,} | {os_a.get('total_tables', 0):,} |")
    w(f"| 总存储 | {format_size(cn.get('total_size', 0))} | {format_size(os_a.get('total_size', 0))} |")
    w(f"| 托管表 | {cn.get('managed_tables', 0):,} | {os_a.get('managed_tables', 0):,} |")
    w(f"| 视图 | {cn.get('virtual_views', 0):,} | {os_a.get('virtual_views', 0):,} |")
    w(f"| 30天活跃 | {cn.get('active_30d', 0):,} | {os_a.get('active_30d', 0):,} |")
    w(f"| >1年未更新 | {cn.get('stale_over_1y', 0):,} | {os_a.get('stale_over_1y', 0):,} |")
    w(f"| 未设生命周期 | {cn.get('no_lifecycle', 0):,} | {os_a.get('no_lifecycle', 0):,} |")
    w(f"| 无注释表 | {cn.get('tables_no_comment', 0):,} | {os_a.get('tables_no_comment', 0):,} |")
    w("")

    # ── 治理建议 ──
    w("## 四、治理建议\n")

    total_stale = cn.get("stale_over_1y", 0) + os_a.get("stale_over_1y", 0)
    total_no_lc = cn.get("no_lifecycle", 0) + os_a.get("no_lifecycle", 0)
    total_no_comment = cn.get("tables_no_comment", 0) + os_a.get("tables_no_comment", 0)

    w("### 4.1 存储优化")
    w(f"- 超过 **1 年未更新**的表共 **{total_stale:,}** 张，建议逐一排查是否可下线或归档")
    w(f"- 未设置生命周期的表 **{total_no_lc:,}** 张，建议根据业务需求设置合理的生命周期")
    w(f"- TMP 临时表共 **{cn.get('layer_dist', {}).get('TMP (临时表)', 0) + os_a.get('layer_dist', {}).get('TMP (临时表)', 0):,}** 张，建议定期清理")
    w("")

    w("### 4.2 数据质量")
    w(f"- 缺少注释的表 **{total_no_comment:,}** 张，建议补充表注释提升可维护性")
    w(f"- 建议建立表命名规范 review 机制，确保分层前缀和业务标识统一")
    w("")

    w("### 4.3 权限管理")
    w(f"- 表 Owner 较为集中，Top 3 Owner 占比超过大部分表")
    w(f"- 建议定期 review 离职/转岗人员的表 Owner 归属")
    w("")

    w("---\n")
    w(f"*报告由 mc_table_analyzer 自动生成 · {NOW.strftime('%Y-%m-%d %H:%M:%S')}*\n")

    return "\n".join(lines)


def main():
    print("📖 加载数据...")
    data = load_data()

    analyses = {}
    for sname in TARGET_SPACES:
        if sname not in data:
            print(f"  ⚠️  未找到 {sname} 的数据")
            continue
        tables = data[sname].get("tables", [])
        print(f"📊 分析 {sname} ({len(tables):,} 张表) ...")
        analyses[sname] = analyze_space(sname, tables)

    print("📝 生成报告...")
    report = generate_report(analyses)

    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"✅ 报告已保存: {REPORT_FILE}")

    # 同时输出 JSON 分析结果
    json_file = REPORT_FILE.replace(".md", ".json")
    with open(json_file, "w", encoding="utf-8") as f:
        # 去掉 top_large_tables 中的 tuple，转为 dict
        out = {}
        for sname, a in analyses.items():
            ac = dict(a)
            ac["top_large_tables"] = [
                {"table_name": t[0], "size": t[1], "size_display": format_size(t[1]),
                 "type": t[2], "owner": t[3], "comment": t[4],
                 "life_cycle": t[5], "creation_time": t[6], "last_modified_time": t[7]}
                for t in a["top_large_tables"]
            ]
            out[sname] = ac
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON 数据: {json_file}")


if __name__ == "__main__":
    main()
