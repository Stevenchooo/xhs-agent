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
