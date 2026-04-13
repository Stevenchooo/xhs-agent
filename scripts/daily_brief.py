"""每日内容简报 - 供 OpenClaw cron 调用"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from xhs_agent.daily import get_today_package

def main():
    pkg = get_today_package()

    print(f"📅 {pkg.get('date', '')} {pkg.get('weekday', '')}  建议发布时间：{pkg.get('time', '')}")
    print(f"📌 今日主题：{pkg.get('theme', '')}")
    print(f"🏷️  类型：{pkg.get('type', '')}")
    print(f"💡 选题理由：{pkg.get('why', '')}\n")

    if pkg.get("data_driven_note"):
        print("=" * 60)
        print("📈 数据驱动说明：")
        print(pkg["data_driven_note"])
        print()

    if pkg.get("tool_focus"):
        print("=" * 60)
        print("🛠️ 今日工具优先级：")
        for t in pkg["tool_focus"]:
            print(f"  · {t.get('name', '')}")
            print(f"    原因：{t.get('reason', '')}")
            print(f"    行动：{t.get('action', '')}")
        print()

    if pkg.get("execution_focus"):
        print("=" * 60)
        print("📌 今日执行重点：")
        for i, line in enumerate(pkg["execution_focus"], 1):
            print(f"  {i}. {line}")
        print()

    if pkg.get("follow_conversion_todo"):
        print("=" * 60)
        print("🎯 今日转粉 TODO：")
        for i, line in enumerate(pkg["follow_conversion_todo"], 1):
            print(f"  {i}. {line}")
        print()

    templates = pkg.get("follow_conversion_templates") or {}
    if templates:
        print("=" * 60)
        print("🧩 转粉固定模板：")
        if templates.get("series_name"):
            print(f"  · 系列名：{templates['series_name']}")
        if templates.get("profile_bio"):
            print(f"  · 主页简介：{templates['profile_bio']}")
        if templates.get("title_formula"):
            print(f"  · 标题结构：{templates['title_formula']}")
        if templates.get("cover_badge"):
            print(f"  · 封面角标：{templates['cover_badge']}")
        if templates.get("ending_line"):
            print(f"  · 正文收尾：{templates['ending_line']}")
        if templates.get("sticky_comment"):
            print(f"  · 置顶评论：{templates['sticky_comment']}")
        if templates.get("pinned_posts"):
            print("  · 置顶3篇：")
            for item in templates["pinned_posts"]:
                print(f"    - {item}")
        print()

    print("=" * 60)
    print("📝 标题：")
    print(pkg.get('title', ''))
    print()

    print("=" * 60)
    print("🎨 Midjourney Prompts：")
    for i, p in enumerate(pkg.get('prompts', []), 1):
        print(f"\n[图{i}] {p.get('desc', '')}")
        print(f"Prompt: {p.get('prompt', '')}")
        if p.get('note'):
            print(f"备注: {p['note']}")

    print()
    print("=" * 60)
    print("📄 正文：")
    print(pkg.get('body', ''))
    print()

    print("=" * 60)
    print("🔖 话题标签：")
    print(pkg.get('hashtags', ''))

if __name__ == '__main__':
    main()
