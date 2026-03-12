#!/usr/bin/env python3
"""
批量执行表/字段 Comment 更新
先修改单表验证，确认无误后可批量执行
"""
import os
import json
from odps import ODPS

# ─── 配置 ───
ACCESS_KEY_ID = os.getenv("DW_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("DW_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

CN_ENDPOINT = "http://service.cn-beijing.maxcompute.aliyun.com/api"
SG_ENDPOINT = "http://service.ap-southeast-1.maxcompute.aliyun.com/api"
SG_PROJECTS = {"tapdb_one_data_asia", "tapdb_one_data_etheria_os", "tapdb_one_data_torchlight_os",
               "tapdb_one_data_asia_t3_os", "tapdb_one_data_asia_fp_os", "xd_ops_sg",
               "xd_game_audit_asia", "tapdb_one_data_asia_ssrpg_os", "tapdb_one_data_asia_ro_os"}

SUGGESTIONS_FILE = os.path.join(os.path.dirname(__file__), "output", "comment_suggestions.json")
GLOSSARY_FILE = os.path.join(os.path.dirname(__file__), "game_glossary.json")


def get_odps(project: str) -> ODPS:
    endpoint = SG_ENDPOINT if project in SG_PROJECTS else CN_ENDPOINT
    return ODPS(ACCESS_KEY_ID, ACCESS_KEY_SECRET, project=project, endpoint=endpoint)


def apply_table_comment(odps: ODPS, table_name: str, comment: str, dry_run: bool = True):
    """修改表的 comment"""
    comment_escaped = comment.replace("'", "\\'")
    sql = f"ALTER TABLE {table_name} SET COMMENT '{comment_escaped}';"
    if dry_run:
        print(f"  [DRY-RUN] {sql}")
    else:
        print(f"  [EXEC] {sql}")
        odps.execute_sql(sql)


def apply_column_comments(odps: ODPS, table_name: str, col_comments: dict, dry_run: bool = True):
    """修改字段的 comment"""
    # MaxCompute: ALTER TABLE xxx CHANGE COLUMN col_name COMMENT 'xxx'
    for col_name, comment in col_comments.items():
        # 转义单引号
        comment_escaped = comment.replace("'", "\\'")
        sql = f"ALTER TABLE {table_name} CHANGE COLUMN {col_name} COMMENT '{comment_escaped}';"
        if dry_run:
            print(f"  [DRY-RUN] {sql}")
        else:
            print(f"  [EXEC] {sql}")
            try:
                odps.execute_sql(sql)
            except Exception as e:
                print(f"  ⚠️  失败: {e}")


def apply_single_table(project: str, table_name: str, dry_run: bool = True):
    """修改指定的单张表的 comment（优先用建议文件，兜底实时推断）"""
    target = None

    # 1. 先从建议文件查找
    if os.path.exists(SUGGESTIONS_FILE):
        with open(SUGGESTIONS_FILE, "r", encoding="utf-8") as f:
            suggestions = json.load(f)
        for t in suggestions.get(project, {}).get("tables", []):
            if t["table_name"] == table_name:
                target = t
                break

    # 2. 找不到则实时连接 MC 推断
    if not target:
        print(f"ℹ️  建议文件中无此表，实时推断注释...")
        target = infer_comments_live(project, table_name)
        if not target:
            return

    print(f"📋 表: {project}.{table_name}")
    print(f"   建议表注释: {target['suggested_comment']}")
    col_suggestions = target.get("col_comment_suggestions", {})
    print(f"   字段注释建议: {len(col_suggestions)} 个")
    print(f"   模式: {'DRY-RUN (仅打印SQL)' if dry_run else '🔴 实际执行'}")
    print()

    odps = get_odps(project)

    # 修改表注释
    apply_table_comment(odps, table_name, target["suggested_comment"], dry_run=dry_run)

    # 修改字段注释
    if col_suggestions:
        apply_column_comments(odps, table_name, col_suggestions, dry_run=dry_run)

    print(f"\n{'✅ DRY-RUN 完成' if dry_run else '✅ 执行完成'}")


def infer_comments_live(project: str, table_name: str) -> dict:
    """实时连接 MC 获取表结构，用知识库推断注释"""
    from comment_analyzer import parse_table_name, get_game_field_comment, load_game_glossary

    odps = get_odps(project)
    try:
        t = odps.get_table(table_name)
        t.reload()
    except Exception as e:
        print(f"❌ 获取表失败: {e}")
        return None

    parsed = parse_table_name(table_name)
    game_id = parsed.get("game", "")

    # 生成表注释
    parts = []
    if parsed.get("game_cn"):
        parts.append(parsed["game_cn"])
    if parsed.get("region_cn"):
        parts.append(parsed["region_cn"])
    topics = parsed.get("topics", [])
    if topics:
        parts.append("_".join(topics[:3]))
    if parsed.get("layer_cn"):
        parts.append(f"({parsed['layer_cn']})")
    if parsed.get("granularity_cn"):
        parts.append(f"[{parsed['granularity_cn']}]")
    suggested_comment = " ".join(parts) if parts else table_name

    # 生成字段注释
    col_suggestions = {}
    for col in t.table_schema.simple_columns:
        if not col.comment:
            gl = get_game_field_comment(game_id, col.name)
            if gl:
                col_suggestions[col.name] = gl

    return {
        "table_name": table_name,
        "suggested_comment": suggested_comment,
        "col_comment_suggestions": col_suggestions,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="应用表/字段 Comment")
    parser.add_argument("--project", default="tapdb_one_data", help="MC项目名")
    parser.add_argument("--table", required=True, help="表名")
    parser.add_argument("--execute", action="store_true", help="实际执行 (不加此参数则仅打印SQL)")
    args = parser.parse_args()

    apply_single_table(args.project, args.table, dry_run=not args.execute)
