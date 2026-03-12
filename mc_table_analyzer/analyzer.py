#!/usr/bin/env python3
"""
MaxCompute 全空间表分析器
通过 DataWorks API 获取所有工作空间，再用 PyODPS 直连每个 MC 项目列出表信息
"""
import os
import sys
import json
import time
from datetime import datetime
from collections import defaultdict

from odps import ODPS
from alibabacloud_dataworks_public20240518.client import Client as DataWorksClient
from alibabacloud_tea_openapi.models import Config
from alibabacloud_dataworks_public20240518.models import ListProjectsRequest

# ─── 输出目录 ───
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# ─── 双区域配置 ───
REGIONS = {
    "cn-beijing": {
        "dw_endpoint": "dataworks.cn-beijing.aliyuncs.com",
        "mc_endpoint": "http://service.cn-beijing.maxcompute.aliyun.com/api",
    },
    "ap-southeast-1": {
        "dw_endpoint": "dataworks.ap-southeast-1.aliyuncs.com",
        "mc_endpoint": "http://service.ap-southeast-1.maxcompute.aliyun.com/api",
    },
}

# ─── 表分层关键词 ───
LAYER_PREFIXES = {
    "ods": "ODS (原始层)",
    "dwd": "DWD (明细层)",
    "dws": "DWS (汇总层)",
    "dim": "DIM (维度层)",
    "ads": "ADS (应用层)",
    "tmp": "TMP (临时表)",
    "stg": "STG (暂存层)",
}


# ═══════════════════════════════════════════════════════
#  凭证
# ═══════════════════════════════════════════════════════
def get_credentials():
    ak = os.getenv("DW_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("DW_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not ak or not sk:
        raise RuntimeError("缺少凭证，请设置 DW_ACCESS_KEY_ID / DW_ACCESS_KEY_SECRET")
    return ak, sk


# ═══════════════════════════════════════════════════════
#  DataWorks: 列出所有工作空间
# ═══════════════════════════════════════════════════════
def create_dw_client(endpoint: str) -> DataWorksClient:
    ak, sk = get_credentials()
    return DataWorksClient(Config(
        access_key_id=ak, access_key_secret=sk, endpoint=endpoint
    ))


def list_all_projects(client: DataWorksClient) -> list:
    """分页获取所有 DataWorks 工作空间"""
    all_projects = []
    page = 1
    while True:
        req = ListProjectsRequest(page_number=page, page_size=100)
        resp = client.list_projects(req)
        body = resp.body.to_map()
        projects = body.get("PagingInfo", {}).get("Projects", [])
        all_projects.extend(projects)
        total = body.get("PagingInfo", {}).get("TotalCount", 0)
        if page * 100 >= total:
            break
        page += 1
    return all_projects


# ═══════════════════════════════════════════════════════
#  PyODPS: 获取某个 MC 项目的所有表
# ═══════════════════════════════════════════════════════
def list_tables_via_odps(project_name: str, mc_endpoint: str) -> list:
    """使用 INFORMATION_SCHEMA.TABLES 一次性查询所有表，速度远快于逐个遍历"""
    ak, sk = get_credentials()
    odps = ODPS(ak, sk, project=project_name, endpoint=mc_endpoint)

    sql = """
    SELECT
        table_name,
        table_comment,
        owner_name,
        table_type,
        create_time,
        last_modified_time,
        data_length,
        life_cycle
    FROM INFORMATION_SCHEMA.TABLES
    """

    tables_info = []
    try:
        with odps.execute_sql(sql).open_reader() as reader:
            for row in reader:
                tables_info.append({
                    "table_name": str(row["table_name"] or ""),
                    "comment": str(row["table_comment"] or ""),
                    "owner": str(row["owner_name"] or ""),
                    "type": str(row["table_type"] or "TABLE"),
                    "creation_time": str(row["create_time"] or ""),
                    "last_modified_time": str(row["last_modified_time"] or ""),
                    "size": int(row["data_length"] or 0),
                    "life_cycle": int(row["life_cycle"] or 0),
                })
    except Exception:
        # 如果 INFORMATION_SCHEMA 不可用，回退到简单列表
        for t in odps.list_tables():
            tables_info.append({
                "table_name": t.name,
                "owner": "",
                "comment": "",
                "type": "TABLE",
                "creation_time": "",
                "last_modified_time": "",
                "size": 0,
                "life_cycle": 0,
            })
    return tables_info


# ═══════════════════════════════════════════════════════
#  表名分层判断
# ═══════════════════════════════════════════════════════
def classify_layer(table_name: str) -> str:
    name_lower = table_name.lower()
    for prefix, label in LAYER_PREFIXES.items():
        if name_lower.startswith(prefix + "_"):
            return label
    return "其他"


# ═══════════════════════════════════════════════════════
#  分析单个空间的表
# ═══════════════════════════════════════════════════════
def analyze_tables(tables: list) -> dict:
    layer_dist = defaultdict(int)
    owner_dist = defaultdict(int)
    total_size = 0
    table_names = []

    for t in tables:
        tname = t.get("table_name", "")
        table_names.append(tname)
        layer_dist[classify_layer(tname)] += 1
        owner = t.get("owner", "未知")
        owner_dist[owner] += 1
        total_size += t.get("size", 0)

    return {
        "table_count": len(tables),
        "total_size_bytes": total_size,
        "total_size_display": format_size(total_size),
        "layer_distribution": dict(layer_dist),
        "owner_distribution": dict(owner_dist),
        "table_names": table_names,
    }


def format_size(size_bytes: int) -> str:
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


# ═══════════════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════════════
def run(skip_projects: list = None):
    skip_projects = skip_projects or []

    # 1. 遍历所有区域获取工作空间列表
    all_projects = []
    for region, cfg in REGIONS.items():
        print(f"🔍 正在获取 [{region}] 区域的工作空间...")
        try:
            dw = create_dw_client(cfg["dw_endpoint"])
            projects = list_all_projects(dw)
            for p in projects:
                p["_region"] = region
                p["_mc_endpoint"] = cfg["mc_endpoint"]
            all_projects.extend(projects)
            print(f"   ✅ {region} 共 {len(projects)} 个工作空间")
        except Exception as exc:
            print(f"   ⚠️  {region} 获取失败: {exc}")

    print(f"\n✅ 全部区域共发现 {len(all_projects)} 个工作空间\n")

    # 2. 遍历每个空间，通过 PyODPS 拉取表
    report = {}
    summary_rows = []
    total_tables = 0
    total_size = 0

    for idx, proj in enumerate(all_projects, 1):
        pname = proj.get("Name", "")
        display = proj.get("DisplayName", pname)
        status = proj.get("Status", "")
        desc = proj.get("Description", "")
        region = proj.get("_region", "")
        mc_endpoint = proj.get("_mc_endpoint", "")

        if pname in skip_projects:
            print(f"[{idx}/{len(all_projects)}] ⏭️  跳过 {display} ({pname})")
            continue

        if status != "Available":
            print(f"[{idx}/{len(all_projects)}] ⏭️  跳过非可用空间 {display} (状态: {status})")
            continue

        print(f"[{idx}/{len(all_projects)}] 📂 [{region}] {display} ({pname}) ...", end=" ", flush=True)

        try:
            tables = list_tables_via_odps(pname, mc_endpoint)
            analysis = analyze_tables(tables)
            total_tables += analysis["table_count"]
            total_size += analysis["total_size_bytes"]

            report[pname] = {
                "region": region,
                "display_name": display,
                "description": desc,
                **analysis,
                "tables_detail": tables,
            }
            print(f"共 {analysis['table_count']} 张表, {analysis['total_size_display']}")

            summary_rows.append({
                "区域": region,
                "空间名": display,
                "标识": pname,
                "表数量": analysis["table_count"],
                "存储": analysis["total_size_display"],
                "分层": analysis["layer_distribution"],
            })
        except Exception as exc:
            err_msg = str(exc)
            # 精简错误信息
            if "NoSuchObject" in err_msg or "not found" in err_msg.lower():
                print(f"⚠️  MC项目不存在，跳过")
            elif "Forbidden" in err_msg or "denied" in err_msg.lower():
                print(f"⚠️  无权限访问，跳过")
            else:
                print(f"⚠️  失败: {err_msg[:80]}")

            report[pname] = {
                "region": region,
                "display_name": display,
                "description": desc,
                "table_count": 0,
                "error": err_msg[:200],
            }
            summary_rows.append({
                "区域": region,
                "空间名": display,
                "标识": pname,
                "表数量": "❌",
                "存储": "-",
                "分层": {},
            })

        time.sleep(0.1)

    # 3. 全局汇总
    global_layer = defaultdict(int)
    global_owner = defaultdict(int)
    for info in report.values():
        for layer, cnt in info.get("layer_distribution", {}).items():
            global_layer[layer] += cnt
        for owner, cnt in info.get("owner_distribution", {}).items():
            global_owner[owner] += cnt

    summary = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_projects_scanned": len(report),
        "total_tables": total_tables,
        "total_size_display": format_size(total_size),
        "global_layer_distribution": dict(global_layer),
        "global_owner_distribution": dict(global_owner),
        "projects": {k: {kk: vv for kk, vv in v.items() if kk != "tables_detail"}
                     for k, v in report.items()},
    }

    # 4. 保存结果
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 汇总报告 (不含每张表明细)
    out_summary = os.path.join(OUTPUT_DIR, "mc_tables_report.json")
    with open(out_summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # 详细表列表 (含每张表信息)
    out_detail = os.path.join(OUTPUT_DIR, "mc_tables_detail.json")
    detail_data = {}
    for pname, info in report.items():
        if "tables_detail" in info:
            detail_data[pname] = {
                "region": info.get("region"),
                "display_name": info.get("display_name"),
                "table_count": info.get("table_count"),
                "tables": info.get("tables_detail"),
            }
    with open(out_detail, "w", encoding="utf-8") as f:
        json.dump(detail_data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 汇总报告: {out_summary}")
    print(f"💾 详细表列表: {out_detail}")

    # 5. 打印汇总
    print_summary(summary, summary_rows, total_size)


def print_summary(summary: dict, rows: list, total_size: int):
    print("\n" + "═" * 80)
    print("  MaxCompute 全空间表分析报告")
    print(f"  生成时间: {summary['generated_at']}")
    print("═" * 80)
    print(f"\n  📊 总计: {summary['total_projects_scanned']} 个空间, "
          f"{summary['total_tables']} 张表, 总存储 {format_size(total_size)}\n")

    # ── 各空间表数量排行 ──
    sorted_rows = sorted(rows, key=lambda r: r["表数量"] if isinstance(r["表数量"], int) else -1, reverse=True)
    print("  ┌─ 各空间表数量排行 " + "─" * 58 + "┐")
    print(f"  │ {'区域':<16} {'空间名':<22} {'标识':<26} {'表数量':>5} {'存储':>10} │")
    print("  ├" + "─" * 85 + "┤")
    for r in sorted_rows:
        region = r.get("区域", "")[:14]
        name = r["空间名"][:20]
        ident = r["标识"][:24]
        cnt = str(r["表数量"]).rjust(5)
        size = r.get("存储", "-").rjust(10)
        print(f"  │ {region:<16} {name:<22} {ident:<26} {cnt} {size} │")
    print("  └" + "─" * 85 + "┘")

    # ── 全局分层分布 ──
    layer_dist = summary.get("global_layer_distribution", {})
    if layer_dist:
        print("\n  ┌─ 全局表分层分布 " + "─" * 58 + "┐")
        sorted_layers = sorted(layer_dist.items(), key=lambda x: x[1], reverse=True)
        for layer, cnt in sorted_layers:
            pct = cnt / max(1, summary["total_tables"]) * 100
            bar_len = int(pct / 2.5)
            bar = "█" * bar_len
            print(f"  │  {layer:<20} {cnt:>6}  ({pct:5.1f}%)  {bar}")
        print("  └" + "─" * 85 + "┘")

    # ── Top Owner ──
    owner_dist = summary.get("global_owner_distribution", {})
    if owner_dist:
        print("\n  ┌─ 表 Owner Top 10 " + "─" * 58 + "┐")
        sorted_owners = sorted(owner_dist.items(), key=lambda x: x[1], reverse=True)[:10]
        for owner, cnt in sorted_owners:
            print(f"  │  {str(owner)[:50]:<52} {cnt:>6}")
        print("  └" + "─" * 85 + "┘")


# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MaxCompute 全空间表分析器")
    parser.add_argument("--skip", nargs="*", default=[], help="需要跳过的工作空间名称列表")
    args = parser.parse_args()
    run(skip_projects=args.skip)
