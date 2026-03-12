#!/usr/bin/env python3
import os
from odps import ODPS

ak = os.getenv("DW_ACCESS_KEY_ID")
sk = os.getenv("DW_ACCESS_KEY_SECRET")
target = "dws_torchlight_cn_pid_charge_refund_df_tmp"
ep = "http://service.cn-beijing.maxcompute.aliyun.com/api"

projects = [
    "tapdb_one_data", "tapdb_one_data_torchlight", "tapdb_one_data_t3",
    "tapdb_one_data_ro", "tapdb_one_data_fp", "tapdb_one_data_encrypted",
    "xd_game_audit", "tapdb_ad_bj", "tapdb_one_data_xdt",
    "tapdb_one_data_saga", "tapdb_one_data_ssrpg",
]

for proj in projects:
    try:
        odps = ODPS(ak, sk, project=proj, endpoint=ep)
        t = odps.get_table(target)
        t.reload()
        print(f"✅ 找到! 空间: {proj}")
        print(f"   表注释: {t.comment}")
        for col in t.table_schema.simple_columns:
            print(f"   {col.name:30s} {col.type.name:15s} {col.comment or ''}")
        break
    except Exception as e:
        msg = str(e)
        if "not found" in msg.lower() or "NoSuchObject" in msg:
            print(f"  {proj}: 不存在")
        elif "denied" in msg.lower() or "forbidden" in msg.lower():
            print(f"  {proj}: 无权限")
        else:
            print(f"  {proj}: {msg[:80]}")
else:
    print(f"\n❌ 所有空间均未找到 {target}")
