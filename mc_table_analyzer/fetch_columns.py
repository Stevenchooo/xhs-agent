#!/usr/bin/env python3
"""
批量拉取 tapdb_one_data / tapdb_one_data_asia 的全部字段信息
保存到 output/ 下的 JSON 文件，供后续分析使用
"""
import os
import json
import time
from odps import ODPS

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

SPACES = {
    "tapdb_one_data": "http://service.cn-beijing.maxcompute.aliyun.com/api",
    "tapdb_one_data_asia": "http://service.ap-southeast-1.maxcompute.aliyun.com/api",
}


def get_credentials():
    ak = os.getenv("DW_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("DW_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not ak or not sk:
        raise RuntimeError("缺少凭证")
    return ak, sk


def fetch_columns(space_name: str, endpoint: str) -> dict:
    """查询 INFORMATION_SCHEMA.COLUMNS 获取全部字段信息"""
    ak, sk = get_credentials()
    odps = ODPS(ak, sk, project=space_name, endpoint=endpoint)

    sql = """
    SELECT
        table_name,
        column_name,
        column_comment,
        ordinal_position,
        data_type,
        is_nullable
    FROM INFORMATION_SCHEMA.COLUMNS
    """

    print(f"  ⏳ 正在执行 SQL 查询 (可能需要几分钟)...")
    tables = {}
    row_count = 0

    with odps.execute_sql(sql).open_reader() as reader:
        for row in reader:
            tname = str(row["table_name"] or "")
            if tname not in tables:
                tables[tname] = []
            tables[tname].append({
                "col_name": str(row["column_name"] or ""),
                "col_comment": str(row["column_comment"] or ""),
                "position": int(row["ordinal_position"] or 0),
                "col_type": str(row["data_type"] or ""),
                "nullable": str(row["is_nullable"] or ""),
            })
            row_count += 1
            if row_count % 50000 == 0:
                print(f"    已读取 {row_count:,} 行, {len(tables):,} 张表...")

    print(f"  ✅ 共 {row_count:,} 个字段, {len(tables):,} 张表")
    return tables


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for space_name, endpoint in SPACES.items():
        out_file = os.path.join(OUTPUT_DIR, f"columns_{space_name}.json")
        print(f"\n📂 [{space_name}]")

        if os.path.exists(out_file):
            print(f"  ℹ️  文件已存在: {out_file}，跳过 (删除文件可强制重新拉取)")
            continue

        try:
            tables = fetch_columns(space_name, endpoint)
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(tables, f, ensure_ascii=False, indent=1)
            print(f"  💾 已保存: {out_file}")
        except Exception as exc:
            print(f"  ❌ 失败: {exc}")

    print("\n✅ 全部完成")


if __name__ == "__main__":
    main()
