"""小红书运营Agent - 数据复盘与策略调整
输入创作者中心数据 → 对比目标 → 输出调整建议
"""

import json
import os
import datetime
from .config import DATA_DIR

REVIEW_FILE = os.path.join(DATA_DIR, "reviews.json")

# ==================== 阶段目标（基于当前账号近一周数据更新） ====================
# 最新已知状态：主页约35粉，最近9篇笔记中已有2条显著高于均值。
# 当前重点：稳住「名画反差故事」爆款方向，同时提升整体发布稳定性与主页承接。
PHASE_TARGETS = [
    {
        "phase": "Phase 1·冲量验证（当前阶段）",
        "duration": "本周起的2周",
        "date_range": "现在 → +14天",
        "content_target": "累计发满15篇笔记，形成稳定周更节奏",
        "targets": {
            "total_posts": 15,
            "avg_views": 500,
            "avg_likes": 18,
            "avg_saves": 8,
            "followers_gain": 30,
            "best_post_views": 3000,
        },
        "focus": "继续主打「名画反差故事 + 画家价格/技法解释」，同时提高主页承接和稳定更新，让爆款不再只靠单条拉动。",
        "content_mix": [
            "名画反差故事 ×4（天价、反直觉、画家冷知识）",
            "画家故事/人物专题 ×3（持续做系列感）",
            "色彩/审美向内容 ×2（稳收藏和主页氛围）",
            "实验内容 ×1（跨界或破次元壁）",
        ],
    },
    {
        "phase": "Phase 2·找到爆款公式",
        "duration": "第3-4周",
        "date_range": "+14天 → +28天",
        "content_target": "再发9篇（累计24篇）",
        "targets": {
            "total_posts": 24,
            "avg_views": 800,
            "avg_likes": 25,
            "avg_saves": 12,
            "followers_gain": 80,
            "best_post_views": 6000,
        },
        "focus": "把数据最好的2种选题固定成栏目，占比提到60%，同步优化封面模板和评论区互动设计。",
        "content_mix": [
            "数据最好的类型 ×5（主攻方向）",
            "第二好的类型 ×3",
            "实验新方向 ×1",
            "合集/盘点 ×1（冲收藏）",
        ],
    },
    {
        "phase": "Phase 3·稳定增长",
        "duration": "第5-8周",
        "date_range": "+28天 → +56天",
        "content_target": "每周5-7篇",
        "targets": {
            "total_posts": 50,
            "avg_views": 1200,
            "avg_likes": 50,
            "avg_saves": 25,
            "followers_gain": 200,
            "best_post_views": 10000,
        },
        "focus": "固定栏目 + 视频尝试 + 主页转粉优化，把单爆款转成连续增长。",
        "content_mix": [
            "固定栏目内容 ×3/周",
            "视频内容 ×1/周",
            "合集/盘点 ×1/周",
            "热点跟进 ×1/周（有热点时）",
        ],
    },
    {
        "phase": "Phase 4·冲1000粉",
        "duration": "第9-12周",
        "date_range": "+56天 → +84天",
        "content_target": "保持周更5篇",
        "targets": {
            "total_posts": 80,
            "avg_views": 2000,
            "avg_likes": 100,
            "avg_saves": 40,
            "followers_gain": 1000,
            "best_post_views": 50000,
        },
        "focus": "冲击1000粉，完成内容系列化和首页品牌感建设，形成稳定转粉闭环。",
        "content_mix": [
            "2个固定系列栏目",
            "每周1个视频",
            "月度大合集 ×1",
        ],
    },
]


def save_review(data: dict):
    """保存一次数据复盘记录"""
    os.makedirs(DATA_DIR, exist_ok=True)
    reviews = []
    if os.path.exists(REVIEW_FILE):
        try:
            with open(REVIEW_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            reviews = loaded if isinstance(loaded, list) else []
        except (json.JSONDecodeError, OSError, ValueError):
            reviews = []

    data["review_date"] = datetime.datetime.now().isoformat()
    data["review_id"] = len(reviews) + 1
    reviews.append(data)

    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)
    return data["review_id"]


def get_all_reviews() -> list:
    """获取所有复盘记录"""
    if os.path.exists(REVIEW_FILE):
        try:
            with open(REVIEW_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            return loaded if isinstance(loaded, list) else []
        except (json.JSONDecodeError, OSError, ValueError):
            return []
    return []


def get_current_phase(total_posts: int, followers: int) -> dict:
    """根据当前数据判断所处阶段"""
    if total_posts < 10 or followers < 50:
        return PHASE_TARGETS[0]
    elif total_posts < 24 or followers < 200:
        return PHASE_TARGETS[1]
    elif total_posts < 50 or followers < 500:
        return PHASE_TARGETS[2]
    else:
        return PHASE_TARGETS[3]


def evaluate_performance(data: dict) -> dict:
    """评估当前数据表现，给出调整建议"""
    phase = get_current_phase(data.get("total_posts", 0), data.get("followers", 0))
    targets = phase["targets"]

    results = {
        "phase": phase["phase"],
        "overall": "on_track",
        "scores": {},
        "adjustments": [],
        "next_actions": [],
    }

    # 逐项对比
    metrics = [
        ("avg_views", "平均浏览量", "浏览"),
        ("avg_likes", "平均点赞", "点赞"),
        ("avg_saves", "平均收藏", "收藏"),
        ("followers_gain", "涨粉数", "涨粉"),
    ]

    issues = []
    wins = []

    for key, label, short in metrics:
        actual = data.get(key, 0)
        target = targets.get(key, 0)
        if target == 0:
            continue
        ratio = actual / target if target > 0 else 0
        status = "超标" if ratio >= 1.2 else "达标" if ratio >= 0.8 else "偏低" if ratio >= 0.5 else "严重不足"

        results["scores"][label] = {
            "actual": actual,
            "target": target,
            "ratio": round(ratio * 100),
            "status": status,
        }

        if ratio < 0.5:
            issues.append((short, actual, target))
            results["overall"] = "needs_attention"
        elif ratio < 0.8:
            issues.append((short, actual, target))
        elif ratio >= 1.2:
            wins.append((short, actual, target))

    # 生成调整建议
    for short, actual, target in issues:
        if short == "浏览":
            results["adjustments"].extend([
                "🔴 浏览量偏低 → 检查标题是否有「信息缺口」（让人不点就亏的感觉）",
                "🔴 封面图是否在手机小图下依然吸引人？自己发完用另一个手机看效果",
                "🔴 发布时间是否在21:00-22:00？偏移30分钟浏览量差30-50%",
                "🔴 尝试在标题里加数字（如「5个」「3分钟」「10幅」），数字标题点击率高20-40%",
            ])
        elif short == "点赞":
            results["adjustments"].extend([
                "🟡 点赞偏低 → 封面图要更有视觉冲击力，画作要选色彩强烈的",
                "🟡 在正文结尾加一句有「金句感」的总结，引发情感共鸣",
                "🟡 尝试加入更多个人感受（不只是信息搬运，要有「我」的声音）",
            ])
        elif short == "收藏":
            results["adjustments"].extend([
                "🟡 收藏偏低 → 增加干货密度：分享Prompt原文、配色方案、画家清单",
                "🟡 多做合集/清单/教程类内容（收藏率是普通内容的2-3倍）",
                "🟡 在文末加「先🌟Mark住，下次画画时翻出来看」",
            ])
        elif short == "涨粉":
            results["adjustments"].extend([
                "🔴 涨粉慢 → 每天在相关话题下留5条有深度的评论引流",
                "🔴 在每篇笔记结尾加一句稳定关注引导，例如「想继续看名画故事和油画审美内容，可以点个关注」",
                "🔴 主页简介是否清晰表达了你是做什么的？访客3秒内要能判断要不要关注",
            ])

    for short, actual, target in wins:
        results["adjustments"].append(
            f"🟢 {short}表现好（{actual} vs 目标{target}）→ 继续保持这类内容的方向！分析做得好的几篇有什么共同点"
        )

    # 下一步行动
    total_posts = data.get("total_posts", 0)
    if total_posts < 5:
        results["next_actions"] = [
            f"📌 当务之急：你才发了{total_posts}篇，先发到10篇再说其他的",
            "📌 打开Agent的「📌 今日执行」页面，按里面的Prompt和文案每天发1篇",
            "📌 不要纠结完美，先发出去，用数据说话",
        ]
    elif total_posts < 10:
        results["next_actions"] = [
            f"📌 继续发，还差{10 - total_posts}篇到Phase 1目标",
            "📌 回头看已发的笔记，哪篇数据最好？下一篇发同类型的",
            "📌 每天在「名画」「油画」「画家故事」相关话题下留3-5条有内容的评论",
        ]
    else:
        best_type = data.get("best_type", "未知")
        results["next_actions"] = [
            f"📌 你的最佳内容类型是「{best_type}」，下周60%的内容做这个方向",
            "📌 尝试做一个固定栏目（如「每周二·陌生画派推荐」）",
            "📌 试一条视频内容（AI创作过程录屏+字幕，3分钟）",
        ]

    return results
