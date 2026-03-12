"""小红书运营Agent - 数据复盘与策略调整
输入创作者中心数据 → 对比目标 → 输出调整建议
"""

import json
import os
import datetime
from .config import DATA_DIR

REVIEW_FILE = os.path.join(DATA_DIR, "reviews.json")

# ==================== 阶段目标（基于第1周真实数据更新） ====================
# 第1周数据：曝光386 观看28 点赞7(25%) 收藏2(7.1%) 评论1(3.6%) 封面CTR6.3% 涨粉+2 主页访客4→关注2(50%)
# 结论：互动率全部超标（质量OK）但曝光量极低（量不够）
PHASE_TARGETS = [
    {
        "phase": "Phase 1·冲量验证（当前阶段）",
        "duration": "本周起的2周",
        "date_range": "现在 → +14天",
        "content_target": "发满10篇笔记（目前约2篇，还差8篇）",
        "targets": {
            "total_posts": 10,
            "avg_views": 100,
            "avg_likes": 8,
            "avg_saves": 4,
            "followers_gain": 30,
            "best_post_views": 500,
        },
        "focus": "互动率已经很好不用改内容方向，纯粹加发布量+加评论区引流。目标：让算法看到你是活跃创作者",
        "content_mix": [
            "视觉反转型 ×2（放大AI油画10倍，对标#油画Top1，冲高流量）",
            "画家合集/清单 ×3（收藏率最高的类型，且你的收藏率7.1%已验证有效）",
            "AI教程/提示词 ×2（已验证有效：封面CTR6.3%+25%点赞率）",
            "节日热点 ×1（妇女节女画家，蹭节日流量）",
            "AI vs 原作对比 ×2（制造评论区讨论，提升评论率）",
        ],
    },
    {
        "phase": "Phase 2·找到爆款公式",
        "duration": "第3-4周",
        "date_range": "+14天 → +28天",
        "content_target": "再发14篇（累计24篇）",
        "targets": {
            "total_posts": 24,
            "avg_views": 500,
            "avg_likes": 25,
            "avg_saves": 15,
            "followers_gain": 200,
            "best_post_views": 3000,
        },
        "focus": "Phase1里数据最好的2种类型，占比提到60%。开始评论区引流",
        "content_mix": [
            "数据最好的类型 ×8（主攻方向）",
            "第二好的类型 ×3",
            "实验新方向 ×2",
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
            "avg_views": 1000,
            "avg_likes": 50,
            "avg_saves": 30,
            "followers_gain": 500,
            "best_post_views": 10000,
        },
        "focus": "固定栏目+视频尝试+粉丝群建设",
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
            "avg_saves": 60,
            "followers_gain": 1000,
            "best_post_views": 50000,
        },
        "focus": "冲击1000粉开通蒲公英，内容系列化，个人风格成型",
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
        with open(REVIEW_FILE, "r", encoding="utf-8") as f:
            reviews = json.load(f)

    data["review_date"] = datetime.datetime.now().isoformat()
    data["review_id"] = len(reviews) + 1
    reviews.append(data)

    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)
    return data["review_id"]


def get_all_reviews() -> list:
    """获取所有复盘记录"""
    if os.path.exists(REVIEW_FILE):
        with open(REVIEW_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
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
    phase = get_current_phase(data.get("total_posts", 0), data.get("followers", 9))
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
                "🔴 在每篇笔记结尾加「喜欢当代艺术的话，关注我不迷路🎨」",
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
            "📌 每天在「当代艺术」「油画」话题下留3-5条有内容的评论",
        ]
    else:
        best_type = data.get("best_type", "未知")
        results["next_actions"] = [
            f"📌 你的最佳内容类型是「{best_type}」，下周60%的内容做这个方向",
            "📌 尝试做一个固定栏目（如「每周二·陌生画派推荐」）",
            "📌 试一条视频内容（AI创作过程录屏+字幕，3分钟）",
        ]

    return results
