"""小红书运营Agent - 数据复盘与策略调整
输入创作者中心数据 → 对比目标 → 输出调整建议
"""

import json
import os
import datetime
from .config import DATA_DIR

REVIEW_FILE = os.path.join(DATA_DIR, "reviews.json")

# ==================== 阶段目标（基于当前账号近一周数据更新） ====================
# 最新已知状态：最近 7 条笔记里，经典游戏 IP 真人化方向明显跑赢其他题材。
# 当前重点：稳住「游戏角色来到现实世界 / 真人化」方向，减少低效混发，打透晚间黄金时段。
PHASE_TARGETS = [
    {
        "phase": "Phase 1·冲量验证（当前阶段）",
        "duration": "本周起的2周",
        "date_range": "现在 → +14天",
        "content_target": "累计发满15篇笔记，形成稳定周更节奏",
        "targets": {
            "total_posts": 15,
            "avg_views": 700,
            "avg_likes": 20,
            "avg_saves": 6,
            "followers_gain": 30,
            "best_post_views": 3000,
        },
        "focus": "继续主打「经典游戏IP真人化 + 童年回忆」方向，同时减少与主赛道无关的实验内容，把 20:00-21:00 档位做透。",
        "content_mix": [
            "经典游戏IP真人化 ×4（主力方向）",
            "角色萌系短视频 ×2（补稳定互动）",
            "游戏热点快反 ×1（吃热点红利）",
            "借势实验 ×1（仅在能绑定游戏IP时测试）",
        ],
    },
    {
        "phase": "Phase 2·找到爆款公式",
        "duration": "第3-4周",
        "date_range": "+14天 → +28天",
        "content_target": "再发9篇（累计24篇）",
        "targets": {
            "total_posts": 24,
            "avg_views": 1000,
            "avg_likes": 30,
            "avg_saves": 8,
            "followers_gain": 80,
            "best_post_views": 6000,
        },
        "focus": "把「游戏IP真人化」和「热点快反」固定成栏目，占比提到 60%，同步优化封面模板和评论区投票设计。",
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
            "avg_views": 1500,
            "avg_likes": 50,
            "avg_saves": 12,
            "followers_gain": 200,
            "best_post_views": 10000,
        },
        "focus": "固定栏目 + 系列连更 + 主页转粉优化，把单条爆款变成连续增长。",
        "content_mix": [
            "经典游戏IP真人化 ×3/周",
            "热点快反 ×1/周",
            "合集/盘点 ×1/周",
            "制作过程/评论互动 ×1/周",
        ],
    },
    {
        "phase": "Phase 4·冲1000粉",
        "duration": "第9-12周",
        "date_range": "+56天 → +84天",
        "content_target": "保持周更5篇",
        "targets": {
            "total_posts": 80,
            "avg_views": 2500,
            "avg_likes": 100,
            "avg_saves": 18,
            "followers_gain": 1000,
            "best_post_views": 50000,
        },
        "focus": "冲击 1000 粉，完成内容系列化和角色宇宙化，让用户一眼知道你是做游戏IP真人化的。",
        "content_mix": [
            "2个固定系列栏目",
            "每周 1 个热点联动",
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

    from .tracker import sync_latest_review_snapshot

    sync_latest_review_snapshot(data)
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
                "🟡 点赞偏低 → 封面首帧要先出现熟悉角色或强反差画面，不要让用户先理解再决定要不要看",
                "🟡 在正文结尾加一句有「金句感」的总结，引发情感共鸣",
                "🟡 尝试加入更多个人感受（不只是信息搬运，要有「我」的声音）",
            ])
        elif short == "收藏":
            results["adjustments"].extend([
                "🟡 收藏偏低 → 增加可复用信息：分享Prompt原文、角色清单、下一期选题列表",
                "🟡 多做合集/清单/教程类内容（收藏率是普通内容的2-3倍）",
                "🟡 在文末加「先🌟Mark住，下次画画时翻出来看」",
            ])
        elif short == "涨粉":
            results["adjustments"].extend([
                "🔴 涨粉慢 → 每天在相关话题下留5条有深度的评论引流",
                "🔴 在每篇笔记结尾加一句稳定关注引导，例如「想继续看经典游戏角色真人化内容，可以点个关注」",
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
            "📌 每天在「马里奥」「任天堂」「游戏角色真人版」「童年回忆」相关话题下留3-5条有内容的评论",
        ]
    else:
        best_type = data.get("best_type", "未知")
        results["next_actions"] = [
            f"📌 你的最佳内容类型是「{best_type}」，下周60%的内容做这个方向",
            "📌 尝试做一个固定栏目（如「如果X来到现实世界」）",
            "📌 试一条系列化视频内容（同一宇宙多角色连续发 2-3 条）",
        ]

    return results
