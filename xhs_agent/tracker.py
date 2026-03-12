"""小红书运营Agent - 数据追踪与分析"""

import json
import os
import datetime
from .config import ANALYTICS_FILE, CONTENT_HISTORY_FILE, DATA_DIR

COMPETITOR_FILE = os.path.join(DATA_DIR, "competitors.json")


def _ensure_dir():
    """确保数据目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(filepath: str) -> dict:
    """加载JSON文件"""
    _ensure_dir()
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_json(filepath: str, data: dict):
    """保存JSON文件"""
    _ensure_dir()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ==================== 账号信息管理 ====================

def save_account_info(info: dict):
    """保存账号基本信息"""
    data = _load_json(ANALYTICS_FILE)
    data["account_info"] = {
        **info,
        "updated_at": datetime.datetime.now().isoformat()
    }
    _save_json(ANALYTICS_FILE, data)


def get_account_info() -> dict:
    """获取账号基本信息"""
    data = _load_json(ANALYTICS_FILE)
    return data.get("account_info", {})


# ==================== 笔记数据记录 ====================

def add_post_record(record: dict):
    """添加一条笔记发布记录"""
    data = _load_json(CONTENT_HISTORY_FILE)
    if "posts" not in data:
        data["posts"] = []

    record["id"] = len(data["posts"]) + 1
    record["created_at"] = datetime.datetime.now().isoformat()
    if "metrics" not in record:
        record["metrics"] = []

    data["posts"].append(record)
    _save_json(CONTENT_HISTORY_FILE, data)
    return record["id"]


def update_post_metrics(post_id: int, metrics: dict):
    """更新笔记的数据指标"""
    data = _load_json(CONTENT_HISTORY_FILE)
    posts = data.get("posts", [])

    for post in posts:
        if post["id"] == post_id:
            metrics["recorded_at"] = datetime.datetime.now().isoformat()
            post["metrics"].append(metrics)
            post["latest_metrics"] = metrics
            break

    _save_json(CONTENT_HISTORY_FILE, data)


def get_all_posts() -> list:
    """获取所有笔记记录"""
    data = _load_json(CONTENT_HISTORY_FILE)
    return data.get("posts", [])


def get_post_by_id(post_id: int) -> dict:
    """根据ID获取笔记记录"""
    posts = get_all_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return {}


# ==================== 数据分析 ====================

def get_overall_stats() -> dict:
    """获取整体数据统计"""
    posts = get_all_posts()
    if not posts:
        return {
            "total_posts": 0,
            "avg_views": 0,
            "avg_likes": 0,
            "avg_saves": 0,
            "avg_comments": 0,
            "avg_shares": 0,
            "best_post": None,
            "worst_post": None,
        }

    posts_with_metrics = [p for p in posts if p.get("latest_metrics")]
    if not posts_with_metrics:
        return {
            "total_posts": len(posts),
            "avg_views": 0,
            "avg_likes": 0,
            "avg_saves": 0,
            "avg_comments": 0,
            "avg_shares": 0,
            "best_post": None,
            "worst_post": None,
        }

    total = len(posts_with_metrics)
    sum_views = sum(p["latest_metrics"].get("views", 0) for p in posts_with_metrics)
    sum_likes = sum(p["latest_metrics"].get("likes", 0) for p in posts_with_metrics)
    sum_saves = sum(p["latest_metrics"].get("saves", 0) for p in posts_with_metrics)
    sum_comments = sum(p["latest_metrics"].get("comments", 0) for p in posts_with_metrics)
    sum_shares = sum(p["latest_metrics"].get("shares", 0) for p in posts_with_metrics)

    best = max(posts_with_metrics, key=lambda p: p["latest_metrics"].get("views", 0))
    worst = min(posts_with_metrics, key=lambda p: p["latest_metrics"].get("views", 0))

    return {
        "total_posts": len(posts),
        "tracked_posts": total,
        "total_views": sum_views,
        "total_likes": sum_likes,
        "total_saves": sum_saves,
        "total_comments": sum_comments,
        "total_shares": sum_shares,
        "avg_views": round(sum_views / total),
        "avg_likes": round(sum_likes / total),
        "avg_saves": round(sum_saves / total),
        "avg_comments": round(sum_comments / total),
        "avg_shares": round(sum_shares / total),
        "avg_like_rate": round((sum_likes / sum_views * 100) if sum_views > 0 else 0, 2),
        "avg_save_rate": round((sum_saves / sum_views * 100) if sum_views > 0 else 0, 2),
        "avg_comment_rate": round((sum_comments / sum_views * 100) if sum_views > 0 else 0, 2),
        "best_post": {
            "id": best["id"],
            "title": best.get("title", "未知"),
            "views": best["latest_metrics"].get("views", 0),
        },
        "worst_post": {
            "id": worst["id"],
            "title": worst.get("title", "未知"),
            "views": worst["latest_metrics"].get("views", 0),
        },
    }


def get_content_type_analysis() -> dict:
    """按内容类型分析表现"""
    posts = get_all_posts()
    posts_with_metrics = [p for p in posts if p.get("latest_metrics")]

    type_stats = {}
    for post in posts_with_metrics:
        ct = post.get("content_type", "未分类")
        if ct not in type_stats:
            type_stats[ct] = {"count": 0, "total_views": 0, "total_likes": 0, "total_saves": 0}
        type_stats[ct]["count"] += 1
        type_stats[ct]["total_views"] += post["latest_metrics"].get("views", 0)
        type_stats[ct]["total_likes"] += post["latest_metrics"].get("likes", 0)
        type_stats[ct]["total_saves"] += post["latest_metrics"].get("saves", 0)

    for ct, stats in type_stats.items():
        count = stats["count"]
        stats["avg_views"] = round(stats["total_views"] / count) if count > 0 else 0
        stats["avg_likes"] = round(stats["total_likes"] / count) if count > 0 else 0
        stats["avg_saves"] = round(stats["total_saves"] / count) if count > 0 else 0

    return type_stats


def get_time_analysis() -> dict:
    """按发布时间分析表现"""
    posts = get_all_posts()
    posts_with_metrics = [p for p in posts if p.get("latest_metrics") and p.get("post_time")]

    time_stats = {}
    for post in posts_with_metrics:
        hour = post.get("post_time", "").split(":")[0] if ":" in post.get("post_time", "") else "未知"
        if hour not in time_stats:
            time_stats[hour] = {"count": 0, "total_views": 0}
        time_stats[hour]["count"] += 1
        time_stats[hour]["total_views"] += post["latest_metrics"].get("views", 0)

    for hour, stats in time_stats.items():
        stats["avg_views"] = round(stats["total_views"] / stats["count"]) if stats["count"] > 0 else 0

    return time_stats


def get_trend_data() -> list:
    """获取数据趋势（按时间排序的浏览量变化）"""
    posts = get_all_posts()
    posts_with_metrics = [p for p in posts if p.get("latest_metrics")]

    trend = []
    for post in sorted(posts_with_metrics, key=lambda p: p.get("created_at", "")):
        trend.append({
            "date": post.get("created_at", "")[:10],
            "title": post.get("title", "")[:20],
            "views": post["latest_metrics"].get("views", 0),
            "likes": post["latest_metrics"].get("likes", 0),
            "saves": post["latest_metrics"].get("saves", 0),
            "comments": post["latest_metrics"].get("comments", 0),
        })

    return trend


# ==================== 竞品追踪 ====================

def add_competitor(info: dict) -> int:
    """添加竞品账号"""
    data = _load_json(COMPETITOR_FILE)
    if "competitors" not in data:
        data["competitors"] = []

    info["id"] = len(data["competitors"]) + 1
    info["created_at"] = datetime.datetime.now().isoformat()
    if "viral_posts" not in info:
        info["viral_posts"] = []
    data["competitors"].append(info)
    _save_json(COMPETITOR_FILE, data)
    return info["id"]


def get_all_competitors() -> list:
    """获取所有竞品账号"""
    data = _load_json(COMPETITOR_FILE)
    return data.get("competitors", [])


def update_competitor(comp_id: int, updates: dict):
    """更新竞品账号信息"""
    data = _load_json(COMPETITOR_FILE)
    for comp in data.get("competitors", []):
        if comp["id"] == comp_id:
            comp.update(updates)
            comp["updated_at"] = datetime.datetime.now().isoformat()
            break
    _save_json(COMPETITOR_FILE, data)


def add_competitor_viral_post(comp_id: int, post_info: dict):
    """为竞品账号添加爆款笔记记录"""
    data = _load_json(COMPETITOR_FILE)
    for comp in data.get("competitors", []):
        if comp["id"] == comp_id:
            post_info["recorded_at"] = datetime.datetime.now().isoformat()
            comp.setdefault("viral_posts", []).append(post_info)
            break
    _save_json(COMPETITOR_FILE, data)


def delete_competitor(comp_id: int):
    """删除竞品账号"""
    data = _load_json(COMPETITOR_FILE)
    data["competitors"] = [c for c in data.get("competitors", []) if c["id"] != comp_id]
    _save_json(COMPETITOR_FILE, data)


def get_competitor_by_id(comp_id: int) -> dict:
    """根据ID获取竞品信息"""
    for comp in get_all_competitors():
        if comp["id"] == comp_id:
            return comp
    return {}


# ==================== 周数据快照 ====================

def save_weekly_snapshot():
    """保存本周的数据快照（用于周报对比）"""
    data = _load_json(ANALYTICS_FILE)
    if "weekly_snapshots" not in data:
        data["weekly_snapshots"] = []

    stats = get_overall_stats()
    snapshot = {
        "date": datetime.datetime.now().isoformat(),
        "week": datetime.datetime.now().strftime("%Y-W%W"),
        **stats,
    }
    data["weekly_snapshots"].append(snapshot)
    _save_json(ANALYTICS_FILE, data)
    return snapshot


def get_weekly_snapshots() -> list:
    """获取所有周数据快照"""
    data = _load_json(ANALYTICS_FILE)
    return data.get("weekly_snapshots", [])


# ==================== 发后追踪 ====================

POST_TRACKING_FILE = os.path.join(DATA_DIR, "post_tracking.json")


def start_post_tracking(post_info: dict) -> int:
    """开始追踪一篇新发布的笔记"""
    data = _load_json(POST_TRACKING_FILE)
    if "tracking" not in data:
        data["tracking"] = []

    tracking = {
        "id": len(data["tracking"]) + 1,
        "title": post_info.get("title", ""),
        "content_type": post_info.get("content_type", ""),
        "publish_time": datetime.datetime.now().isoformat(),
        "status": "tracking",  # tracking / completed
        "checkpoints": {},
    }
    data["tracking"].append(tracking)
    _save_json(POST_TRACKING_FILE, data)
    return tracking["id"]


def record_checkpoint(tracking_id: int, checkpoint_key: str, metrics: dict) -> dict:
    """记录某个检查点的数据"""
    from .config import POST_CHECKPOINTS

    data = _load_json(POST_TRACKING_FILE)
    checkpoint_config = POST_CHECKPOINTS.get(checkpoint_key, {})
    benchmarks = checkpoint_config.get("benchmarks", {})

    result = {"status": "unknown", "details": {}}

    for tracking in data.get("tracking", []):
        if tracking["id"] == tracking_id:
            # 计算各指标是否达标
            details = {}
            all_good = True
            for metric, target in benchmarks.items():
                actual = metrics.get(metric, 0)
                passed = actual >= target
                details[metric] = {
                    "actual": actual,
                    "target": target,
                    "passed": passed,
                    "ratio": round(actual / target * 100) if target > 0 else 0,
                }
                if not passed:
                    all_good = False

            checkpoint_data = {
                "recorded_at": datetime.datetime.now().isoformat(),
                "metrics": metrics,
                "evaluation": details,
                "overall": "good" if all_good else "needs_attention",
            }
            tracking["checkpoints"][checkpoint_key] = checkpoint_data

            # 如果72h检查完了，标记为完成
            if checkpoint_key == "72h":
                tracking["status"] = "completed"

            result = {
                "status": "good" if all_good else "needs_attention",
                "details": details,
                "actions": checkpoint_config.get(
                    "actions_if_good" if all_good else "actions_if_low", []
                ),
            }
            break

    _save_json(POST_TRACKING_FILE, data)
    return result


def get_all_tracking() -> list:
    """获取所有追踪记录"""
    data = _load_json(POST_TRACKING_FILE)
    return data.get("tracking", [])


def get_active_tracking() -> list:
    """获取正在追踪中的笔记"""
    return [t for t in get_all_tracking() if t.get("status") == "tracking"]


def get_tracking_by_id(tracking_id: int) -> dict:
    """根据ID获取追踪记录"""
    for t in get_all_tracking():
        if t["id"] == tracking_id:
            return t
    return {}


# ==================== 互动巡逻记录 ====================

ENGAGEMENT_LOG_FILE = os.path.join(DATA_DIR, "engagement_log.json")


def log_engagement(entry: dict):
    """记录一次互动行为"""
    data = _load_json(ENGAGEMENT_LOG_FILE)
    if "logs" not in data:
        data["logs"] = []

    entry["timestamp"] = datetime.datetime.now().isoformat()
    entry["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
    data["logs"].append(entry)
    _save_json(ENGAGEMENT_LOG_FILE, data)


def get_today_engagement() -> dict:
    """获取今日互动统计"""
    data = _load_json(ENGAGEMENT_LOG_FILE)
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    today_logs = [l for l in data.get("logs", []) if l.get("date") == today]

    comments_count = sum(1 for l in today_logs if l.get("type") == "comment")
    replies_count = sum(1 for l in today_logs if l.get("type") == "reply")
    dms_count = sum(1 for l in today_logs if l.get("type") == "dm")

    return {
        "date": today,
        "total_actions": len(today_logs),
        "comments": comments_count,
        "replies": replies_count,
        "dms": dms_count,
        "logs": today_logs,
    }


def get_engagement_history(days: int = 7) -> list:
    """获取最近N天的互动统计"""
    data = _load_json(ENGAGEMENT_LOG_FILE)
    logs = data.get("logs", [])

    history = {}
    today = datetime.datetime.now()
    for i in range(days):
        date_str = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        day_logs = [l for l in logs if l.get("date") == date_str]
        history[date_str] = {
            "date": date_str,
            "total": len(day_logs),
            "comments": sum(1 for l in day_logs if l.get("type") == "comment"),
            "replies": sum(1 for l in day_logs if l.get("type") == "reply"),
        }

    return sorted(history.values(), key=lambda x: x["date"], reverse=True)


def get_engagement_streak() -> int:
    """计算连续互动天数"""
    data = _load_json(ENGAGEMENT_LOG_FILE)
    logs = data.get("logs", [])

    dates = sorted(set(l.get("date") for l in logs if l.get("date")), reverse=True)
    if not dates:
        return 0

    streak = 0
    today = datetime.datetime.now()
    for i in range(len(dates)):
        expected = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if expected in dates:
            streak += 1
        else:
            break
    return streak


# ==================== 账号健康度计算 ====================

def calculate_account_health() -> dict:
    """计算账号健康度评分"""
    posts = get_all_posts()
    account = get_account_info()
    stats = get_overall_stats()
    engagement = get_engagement_history(14)

    health = {
        "overall_score": 0,
        "dimensions": {},
        "level": "待评估",
        "summary": "",
    }

    if not posts:
        health["summary"] = "暂无数据，请先发布笔记并记录数据"
        return health

    scores = {}

    # 1. 内容一致性（发布频率）
    posts_with_date = [p for p in posts if p.get("post_date")]
    if posts_with_date:
        dates = sorted(set(p["post_date"] for p in posts_with_date))
        if len(dates) >= 2:
            first = datetime.datetime.fromisoformat(dates[0])
            last = datetime.datetime.fromisoformat(dates[-1])
            days_span = max((last - first).days, 1)
            posts_per_week = len(posts_with_date) / days_span * 7
            if posts_per_week >= 5:
                scores["内容一致性"] = 95
            elif posts_per_week >= 3:
                scores["内容一致性"] = 75
            elif posts_per_week >= 1:
                scores["内容一致性"] = 50
            else:
                scores["内容一致性"] = 25
        else:
            scores["内容一致性"] = 30
    else:
        scores["内容一致性"] = 20

    # 2. 互动质量
    if stats.get("avg_views", 0) > 0:
        like_rate = stats.get("avg_like_rate", 0)
        save_rate = stats.get("avg_save_rate", 0)
        comment_rate = stats.get("avg_comment_rate", 0)

        interaction_score = 0
        if like_rate >= 5:
            interaction_score += 35
        elif like_rate >= 3:
            interaction_score += 25
        elif like_rate >= 1:
            interaction_score += 15
        else:
            interaction_score += 5

        if save_rate >= 5:
            interaction_score += 35
        elif save_rate >= 3:
            interaction_score += 25
        elif save_rate >= 1:
            interaction_score += 15
        else:
            interaction_score += 5

        if comment_rate >= 2:
            interaction_score += 30
        elif comment_rate >= 1:
            interaction_score += 20
        elif comment_rate >= 0.5:
            interaction_score += 10
        else:
            interaction_score += 5

        scores["互动质量"] = min(interaction_score, 100)
    else:
        scores["互动质量"] = 0

    # 3. 增长趋势
    snapshots = get_weekly_snapshots()
    if len(snapshots) >= 2:
        recent = snapshots[-1]
        prev = snapshots[-2]
        growth_indicators = 0
        if recent.get("avg_views", 0) > prev.get("avg_views", 0):
            growth_indicators += 1
        if recent.get("avg_likes", 0) > prev.get("avg_likes", 0):
            growth_indicators += 1
        if recent.get("total_posts", 0) > prev.get("total_posts", 0):
            growth_indicators += 1

        scores["增长趋势"] = min(growth_indicators * 33, 100)
    else:
        followers = account.get("followers", 0)
        scores["增长趋势"] = 50 if followers > 0 else 20

    # 4. 内容多样性
    type_stats = get_content_type_analysis()
    unique_types = len(type_stats)
    if unique_types >= 5:
        scores["内容多样性"] = 95
    elif unique_types >= 3:
        scores["内容多样性"] = 70
    elif unique_types >= 2:
        scores["内容多样性"] = 45
    else:
        scores["内容多样性"] = 20

    # 5. 粉丝粘性（用互动巡逻连续天数衡量）
    streak = get_engagement_streak()
    active_days = sum(1 for e in engagement if e.get("total", 0) > 0)
    if streak >= 14:
        scores["粉丝粘性"] = 95
    elif streak >= 7:
        scores["粉丝粘性"] = 75
    elif active_days >= 3:
        scores["粉丝粘性"] = 50
    else:
        scores["粉丝粘性"] = 25

    # 计算加权总分
    from .config import ACCOUNT_HEALTH_DIMENSIONS
    total_score = 0
    for dim_name, dim_info in ACCOUNT_HEALTH_DIMENSIONS.items():
        score = scores.get(dim_name, 0)
        weight = dim_info["weight"]
        total_score += score * weight / 100
        health["dimensions"][dim_name] = {
            "score": score,
            "weight": weight,
            "description": dim_info["description"],
            "level": "优秀" if score >= 80 else "良好" if score >= 60 else "一般" if score >= 40 else "需要改善",
        }

    health["overall_score"] = round(total_score)
    if total_score >= 80:
        health["level"] = "🟢 健康"
    elif total_score >= 60:
        health["level"] = "🟡 良好"
    elif total_score >= 40:
        health["level"] = "🟠 需关注"
    else:
        health["level"] = "🔴 需要改善"

    return health


# ==================== 历史经验引擎 ====================

def get_best_performing_posts(top_n: int = 5, sort_by: str = "views") -> list:
    """获取历史表现最好的N篇笔记（按指定指标排序）"""
    posts = get_all_posts()
    posts_with_metrics = [p for p in posts if p.get("latest_metrics")]
    if not posts_with_metrics:
        return []
    sorted_posts = sorted(
        posts_with_metrics,
        key=lambda p: p["latest_metrics"].get(sort_by, 0),
        reverse=True
    )
    return sorted_posts[:top_n]


def get_worst_performing_posts(top_n: int = 3) -> list:
    """获取历史表现最差的N篇笔记"""
    posts = get_all_posts()
    posts_with_metrics = [p for p in posts if p.get("latest_metrics")]
    if not posts_with_metrics:
        return []
    sorted_posts = sorted(
        posts_with_metrics,
        key=lambda p: p["latest_metrics"].get("views", 0),
    )
    return sorted_posts[:top_n]


def get_dynamic_benchmarks() -> dict:
    """
    根据自身历史数据计算动态基准线，替代固定基准。
    逻辑：以历史Top30%的表现作为「好」的标准，历史均值作为「及格」标准。
    """
    posts = get_all_posts()
    posts_with_metrics = [p for p in posts if p.get("latest_metrics")]

    if len(posts_with_metrics) < 3:
        return {"has_data": False, "message": "需要至少3篇有数据的笔记才能计算动态基准"}

    views_list = sorted([p["latest_metrics"].get("views", 0) for p in posts_with_metrics], reverse=True)
    likes_list = sorted([p["latest_metrics"].get("likes", 0) for p in posts_with_metrics], reverse=True)
    saves_list = sorted([p["latest_metrics"].get("saves", 0) for p in posts_with_metrics], reverse=True)
    comments_list = sorted([p["latest_metrics"].get("comments", 0) for p in posts_with_metrics], reverse=True)

    n = len(views_list)
    top30_idx = max(n // 3, 1)

    def _avg(lst):
        return round(sum(lst) / len(lst)) if lst else 0

    def _top30(lst, idx):
        return round(sum(lst[:idx]) / idx) if idx > 0 else 0

    return {
        "has_data": True,
        "total_posts": n,
        "benchmarks": {
            "views": {
                "avg": _avg(views_list),
                "top30": _top30(views_list, top30_idx),
                "best": views_list[0] if views_list else 0,
            },
            "likes": {
                "avg": _avg(likes_list),
                "top30": _top30(likes_list, top30_idx),
                "best": likes_list[0] if likes_list else 0,
            },
            "saves": {
                "avg": _avg(saves_list),
                "top30": _top30(saves_list, top30_idx),
                "best": saves_list[0] if saves_list else 0,
            },
            "comments": {
                "avg": _avg(comments_list),
                "top30": _top30(comments_list, top30_idx),
                "best": comments_list[0] if comments_list else 0,
            },
        },
    }


def extract_historical_insights() -> dict:
    """
    从所有历史数据中提取可执行的经验洞察。
    这是历史经验引擎的核心函数。
    """
    posts = get_all_posts()
    posts_with_metrics = [p for p in posts if p.get("latest_metrics")]
    stats = get_overall_stats()
    type_stats = get_content_type_analysis()
    time_stats = get_time_analysis()

    insights = {
        "has_data": len(posts_with_metrics) >= 3,
        "total_posts": len(posts),
        "tracked_posts": len(posts_with_metrics),
        "best_content_type": None,
        "worst_content_type": None,
        "best_posting_time": None,
        "best_posting_day": None,
        "content_type_ranking": [],
        "time_ranking": [],
        "day_ranking": [],
        "performance_trend": "unknown",
        "content_mix_suggestion": [],
        "discovered_patterns": [],
        "top_posts": [],
        "bottom_posts": [],
    }

    if not insights["has_data"]:
        return insights

    # 1. 内容类型排名（按平均浏览量）
    if type_stats:
        type_ranking = sorted(
            [(ct, s) for ct, s in type_stats.items()],
            key=lambda x: x[1].get("avg_views", 0),
            reverse=True
        )
        insights["content_type_ranking"] = [
            {
                "type": ct,
                "count": s["count"],
                "avg_views": s["avg_views"],
                "avg_likes": s["avg_likes"],
                "avg_saves": s["avg_saves"],
                "save_rate": round(s["avg_saves"] / s["avg_views"] * 100, 1) if s["avg_views"] > 0 else 0,
            }
            for ct, s in type_ranking
        ]
        if type_ranking:
            insights["best_content_type"] = type_ranking[0][0]
            insights["worst_content_type"] = type_ranking[-1][0]

    # 2. 发布时间排名
    if time_stats:
        time_ranking = sorted(
            [(h, s) for h, s in time_stats.items() if h != "未知"],
            key=lambda x: x[1].get("avg_views", 0),
            reverse=True
        )
        insights["time_ranking"] = [
            {"hour": h, "count": s["count"], "avg_views": s["avg_views"]}
            for h, s in time_ranking
        ]
        if time_ranking:
            insights["best_posting_time"] = f"{time_ranking[0][0]}:00"

    # 3. 星期排名
    day_perf = {}
    for p in posts_with_metrics:
        post_date = p.get("post_date", "")
        if post_date:
            try:
                dt = datetime.datetime.fromisoformat(post_date)
                day_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][dt.weekday()]
                if day_name not in day_perf:
                    day_perf[day_name] = {"count": 0, "total_views": 0}
                day_perf[day_name]["count"] += 1
                day_perf[day_name]["total_views"] += p["latest_metrics"].get("views", 0)
            except (ValueError, IndexError):
                pass

    if day_perf:
        for day, s in day_perf.items():
            s["avg_views"] = round(s["total_views"] / s["count"]) if s["count"] > 0 else 0
        day_ranking = sorted(day_perf.items(), key=lambda x: x[1]["avg_views"], reverse=True)
        insights["day_ranking"] = [
            {"day": d, "count": s["count"], "avg_views": s["avg_views"]}
            for d, s in day_ranking
        ]
        if day_ranking:
            insights["best_posting_day"] = day_ranking[0][0]

    # 4. 表现趋势（最近5篇 vs 之前所有）
    if len(posts_with_metrics) >= 6:
        recent = posts_with_metrics[-5:]
        older = posts_with_metrics[:-5]
        recent_avg = sum(p["latest_metrics"].get("views", 0) for p in recent) / len(recent)
        older_avg = sum(p["latest_metrics"].get("views", 0) for p in older) / len(older)
        if recent_avg > older_avg * 1.2:
            insights["performance_trend"] = "improving"
        elif recent_avg < older_avg * 0.8:
            insights["performance_trend"] = "declining"
        else:
            insights["performance_trend"] = "stable"

    # 5. 内容配比建议（基于历史数据）
    if insights["content_type_ranking"]:
        total_types = len(insights["content_type_ranking"])
        for i, ct_info in enumerate(insights["content_type_ranking"]):
            if i == 0:
                pct = 50 if total_types > 2 else 60
                role = "主力内容（数据最好）"
            elif i == 1:
                pct = 30 if total_types > 2 else 40
                role = "辅助内容"
            else:
                pct = max(20 // (total_types - 2), 5)
                role = "实验内容"
            insights["content_mix_suggestion"].append({
                "type": ct_info["type"],
                "percentage": pct,
                "role": role,
                "reason": f"平均浏览{ct_info['avg_views']}，共发{ct_info['count']}篇",
            })

    # 6. 自动发现的规律
    patterns = []

    # 收藏率最高的内容类型
    if insights["content_type_ranking"]:
        best_save = max(insights["content_type_ranking"], key=lambda x: x.get("save_rate", 0))
        if best_save["save_rate"] > 3:
            patterns.append(f"📊 「{best_save['type']}」的收藏率最高（{best_save['save_rate']}%），说明这类内容干货价值感最强")

    # 浏览量方差大的内容类型（不稳定）
    if len(insights["content_type_ranking"]) >= 2:
        top = insights["content_type_ranking"][0]
        bottom = insights["content_type_ranking"][-1]
        if top["avg_views"] > 0 and bottom["avg_views"] > 0:
            ratio = top["avg_views"] / bottom["avg_views"]
            if ratio > 3:
                patterns.append(f"⚠️ 「{top['type']}」的浏览量是「{bottom['type']}」的{ratio:.0f}倍，考虑减少后者的比例")

    # 趋势洞察
    if insights["performance_trend"] == "improving":
        patterns.append("📈 最近5篇的平均浏览量比之前有明显提升，说明你在找到对的方向！继续保持")
    elif insights["performance_trend"] == "declining":
        patterns.append("📉 最近5篇的平均浏览量有所下降，需要回顾之前数据好的笔记做了什么不同")

    # 发布时间洞察
    if insights["time_ranking"] and len(insights["time_ranking"]) >= 2:
        best_t = insights["time_ranking"][0]
        patterns.append(f"⏰ {best_t['hour']}点发布的笔记平均浏览量最高（{best_t['avg_views']}），建议固定在这个时间发布")

    # 星期洞察
    if insights["day_ranking"] and len(insights["day_ranking"]) >= 2:
        best_d = insights["day_ranking"][0]
        patterns.append(f"📅 {best_d['day']}发布的笔记数据最好（平均{best_d['avg_views']}浏览），优先在这天发重要内容")

    insights["discovered_patterns"] = patterns

    # 7. Top/Bottom posts
    insights["top_posts"] = get_best_performing_posts(3, "views")
    insights["bottom_posts"] = get_worst_performing_posts(3)

    return insights


def build_historical_context_for_ai() -> str:
    """
    构建可注入AI prompt的历史经验上下文摘要。
    供 content.py 的各生成函数使用。
    """
    insights = extract_historical_insights()
    if not insights["has_data"]:
        return ""

    parts = []
    parts.append(f"【账号历史数据参考·{insights['tracked_posts']}篇笔记的经验】")

    # 最佳内容类型
    if insights["best_content_type"]:
        parts.append(f"- 历史数据最好的内容类型：「{insights['best_content_type']}」")

    # 最佳发布时间
    if insights["best_posting_time"]:
        parts.append(f"- 历史数据最好的发布时间：{insights['best_posting_time']}")

    # 最佳星期
    if insights["best_posting_day"]:
        parts.append(f"- 历史数据最好的发布日：{insights['best_posting_day']}")

    # Top 3 笔记标题
    if insights["top_posts"]:
        parts.append("- 历史表现最好的笔记标题：")
        for p in insights["top_posts"][:3]:
            m = p.get("latest_metrics", {})
            parts.append(f"  ✅「{p.get('title', '')}」（{p.get('content_type', '')}）浏览{m.get('views', 0)} 点赞{m.get('likes', 0)} 收藏{m.get('saves', 0)}")

    # Bottom 笔记
    if insights["bottom_posts"]:
        parts.append("- 历史表现最差的笔记标题（避免类似选题/写法）：")
        for p in insights["bottom_posts"][:2]:
            m = p.get("latest_metrics", {})
            parts.append(f"  ❌「{p.get('title', '')}」（{p.get('content_type', '')}）浏览{m.get('views', 0)}")

    # 关键发现
    if insights["discovered_patterns"]:
        parts.append("- 历史数据中发现的关键规律：")
        for pattern in insights["discovered_patterns"][:3]:
            parts.append(f"  {pattern}")

    return "\n".join(parts)


# ==================== 后链路漏斗追踪 ====================

FUNNEL_FILE = os.path.join(DATA_DIR, "funnel_data.json")


def save_funnel_record(record: dict) -> int:
    """保存一条后链路数据记录（单篇笔记或整体账号层面）"""
    data = _load_json(FUNNEL_FILE)
    if "records" not in data:
        data["records"] = []

    record["id"] = len(data["records"]) + 1
    record["recorded_at"] = datetime.datetime.now().isoformat()
    record["date"] = datetime.datetime.now().strftime("%Y-%m-%d")

    # 自动计算衍生指标
    views = record.get("views", 0)
    likes = record.get("likes", 0)
    saves = record.get("saves", 0)
    comments = record.get("comments", 0)
    shares = record.get("shares", 0)
    record["total_engagement"] = likes + saves + comments + shares

    data["records"].append(record)
    _save_json(FUNNEL_FILE, data)
    return record["id"]


def get_all_funnel_records() -> list:
    """获取所有漏斗数据记录"""
    data = _load_json(FUNNEL_FILE)
    return data.get("records", [])


def get_latest_funnel_record() -> dict:
    """获取最新一条漏斗数据"""
    records = get_all_funnel_records()
    return records[-1] if records else {}


def calculate_funnel_rates(record: dict) -> list:
    """
    根据一条漏斗数据计算各环节转化率，并匹配基准和建议动作。
    返回一个列表，每项是一个环节的分析结果。
    """
    from .config import FUNNEL_STAGES

    # 确保 total_engagement 存在
    if "total_engagement" not in record:
        record["total_engagement"] = (
            record.get("likes", 0) + record.get("saves", 0)
            + record.get("comments", 0) + record.get("shares", 0)
        )

    results = []
    for stage in FUNNEL_STAGES:
        from_val = record.get(stage["from_field"], 0)
        to_val = record.get(stage["to_field"], 0)

        # 跳过无数据的环节
        if from_val == 0 and to_val == 0:
            continue

        rate = round(to_val / from_val * 100, 2) if from_val > 0 else 0

        if rate >= stage["benchmark_excellent"]:
            level = "excellent"
            level_label = "🟢 优秀"
        elif rate >= stage["benchmark_good"]:
            level = "good"
            level_label = "🟢 达标"
        elif rate >= stage["benchmark_low"]:
            level = "normal"
            level_label = "🟡 一般"
        else:
            level = "low"
            level_label = "🔴 瓶颈"

        actions = stage["actions_low"] if level in ("low", "normal") else stage["actions_good"]

        results.append({
            "key": stage["key"],
            "name": stage["name"],
            "from_label": stage["from"],
            "to_label": stage["to"],
            "from_value": from_val,
            "to_value": to_val,
            "rate": rate,
            "metric_name": stage["metric_name"],
            "benchmark_low": stage["benchmark_low"],
            "benchmark_good": stage["benchmark_good"],
            "benchmark_excellent": stage["benchmark_excellent"],
            "level": level,
            "level_label": level_label,
            "diagnosis": stage["diagnosis_low"] if level in ("low", "normal") else "",
            "actions": actions,
        })

    return results


def find_funnel_bottleneck(funnel_results: list) -> dict:
    """
    从漏斗分析结果中找到最大瓶颈（转化率最低于基准比例的环节）。
    """
    if not funnel_results:
        return {}

    worst = None
    worst_gap = float("inf")

    for r in funnel_results:
        # 距离「良好」线的差距比例
        if r["benchmark_good"] > 0:
            gap_ratio = r["rate"] / r["benchmark_good"]
        else:
            gap_ratio = 1.0

        if gap_ratio < worst_gap:
            worst_gap = gap_ratio
            worst = r

    return worst if worst else {}


def get_funnel_trend(limit: int = 10) -> list:
    """获取漏斗数据的历史趋势"""
    records = get_all_funnel_records()
    trend = []
    for record in records[-limit:]:
        views = record.get("views", 0)
        total_eng = record.get("total_engagement", 0)
        entry = {
            "date": record.get("date", ""),
            "title": record.get("title", "整体"),
            "scope": record.get("scope", "post"),
            "impressions": record.get("impressions", 0),
            "views": views,
            "engagement": total_eng,
            "ctr": round(views / record["impressions"] * 100, 2) if record.get("impressions", 0) > 0 else 0,
            "engage_rate": round(total_eng / views * 100, 2) if views > 0 else 0,
            "profile_visits": record.get("profile_visits", 0),
            "new_followers": record.get("new_followers", 0),
        }
        trend.append(entry)
    return trend


def get_funnel_comparison() -> dict:
    """
    对比最近两次漏斗数据，计算各环节转化率变化。
    """
    records = get_all_funnel_records()
    if len(records) < 2:
        return {"has_comparison": False}

    current = records[-1]
    previous = records[-2]

    current_rates = {r["key"]: r for r in calculate_funnel_rates(current)}
    previous_rates = {r["key"]: r for r in calculate_funnel_rates(previous)}

    changes = []
    for key, curr in current_rates.items():
        prev = previous_rates.get(key)
        if prev:
            delta = round(curr["rate"] - prev["rate"], 2)
            changes.append({
                "name": curr["name"],
                "metric_name": curr["metric_name"],
                "current_rate": curr["rate"],
                "previous_rate": prev["rate"],
                "delta": delta,
                "direction": "📈 上升" if delta > 0 else "📉 下降" if delta < 0 else "➡️ 持平",
                "current_level": curr["level_label"],
            })

    return {
        "has_comparison": True,
        "current_date": current.get("date", ""),
        "previous_date": previous.get("date", ""),
        "changes": changes,
    }


# ==================== 算法加权评分 & 流量池分析 ====================

def calculate_algorithm_score(metrics: dict) -> dict:
    """
    根据小红书算法权重计算笔记的加权评分。
    权重：关注 ×8 > 评论/转发 ×4 > 点赞/收藏 ×1
    """
    from .config import ALGORITHM_WEIGHTS

    likes = metrics.get("likes", 0)
    saves = metrics.get("saves", 0)
    comments = metrics.get("comments", 0)
    shares = metrics.get("shares", 0)
    new_followers = metrics.get("new_followers", 0)

    raw_score = (
        new_followers * ALGORITHM_WEIGHTS["follow"]["weight"]
        + comments * ALGORITHM_WEIGHTS["comment"]["weight"]
        + shares * ALGORITHM_WEIGHTS["share"]["weight"]
        + likes * ALGORITHM_WEIGHTS["like"]["weight"]
        + saves * ALGORITHM_WEIGHTS["save"]["weight"]
    )

    # 各项贡献分解
    breakdown = {
        "关注": {"count": new_followers, "weight": 8, "score": new_followers * 8},
        "评论": {"count": comments, "weight": 4, "score": comments * 4},
        "转发": {"count": shares, "weight": 4, "score": shares * 4},
        "点赞": {"count": likes, "weight": 1, "score": likes * 1},
        "收藏": {"count": saves, "weight": 1, "score": saves * 1},
    }

    # 找出最大贡献项和最需提升项
    sorted_items = sorted(breakdown.items(), key=lambda x: x[1]["score"], reverse=True)
    top_contributor = sorted_items[0][0] if sorted_items else ""

    # 找出「投入产出比最高的可优化项」
    optimization_priority = []
    if new_followers == 0:
        optimization_priority.append({
            "metric": "关注",
            "reason": "权重×8但当前为0，每增加1个关注=8个点赞的权重",
            "action": "在笔记结尾加「关注不迷路🎨」引导，加强主页吸引力",
        })
    if comments < likes * 0.1:
        optimization_priority.append({
            "metric": "评论",
            "reason": f"评论{comments}条远少于点赞{likes}的10%，权重×4被浪费",
            "action": "文末加低门槛互动问题（二选一/投票/猜答案），每条评论≥15字才算有效",
        })
    if shares == 0:
        optimization_priority.append({
            "metric": "转发",
            "reason": "权重×4但当前为0，分享型内容能快速提升总分",
            "action": "做合集/清单/冷知识类「社交货币」内容，让人忍不住转给朋友",
        })

    return {
        "raw_score": raw_score,
        "breakdown": breakdown,
        "top_contributor": top_contributor,
        "optimization_priority": optimization_priority,
    }


def analyze_traffic_pool(metrics: dict) -> dict:
    """
    分析笔记是否能突破流量池。
    初始曝光200-500，需要：CTR≥8% + 互动率≥5% + 完读率≥45%
    """
    from .config import TRAFFIC_POOL_MODEL

    thresholds = TRAFFIC_POOL_MODEL["breakthrough_thresholds"]
    impressions = metrics.get("impressions", 0)
    views = metrics.get("views", 0)
    total_eng = (
        metrics.get("likes", 0) + metrics.get("saves", 0)
        + metrics.get("comments", 0) + metrics.get("shares", 0)
    )
    completion = metrics.get("completion_rate", 0)

    ctr = round(views / impressions * 100, 2) if impressions > 0 else 0
    eng_rate = round(total_eng / views * 100, 2) if views > 0 else 0

    checks = {
        "ctr": {
            "label": "封面点击率 (CTR)",
            "value": ctr,
            "threshold": thresholds["ctr"]["min"],
            "passed": ctr >= thresholds["ctr"]["min"],
            "unit": "%",
        },
        "engagement_rate": {
            "label": "综合互动率",
            "value": eng_rate,
            "threshold": thresholds["engagement_rate"]["min"],
            "passed": eng_rate >= thresholds["engagement_rate"]["min"],
            "unit": "%",
        },
        "completion_rate": {
            "label": "完读率/完播率",
            "value": completion,
            "threshold": thresholds["completion_rate"]["min"],
            "passed": completion >= thresholds["completion_rate"]["min"] if completion > 0 else None,
            "unit": "%",
        },
    }

    all_passed = all(
        c["passed"] for c in checks.values() if c["passed"] is not None
    )
    passed_count = sum(
        1 for c in checks.values() if c["passed"] is True
    )
    total_checks = sum(
        1 for c in checks.values() if c["passed"] is not None
    )

    # 判断当前可能在哪个流量池
    pool_levels = TRAFFIC_POOL_MODEL["pool_levels"]
    current_pool = pool_levels[0]
    if impressions > 50000:
        current_pool = pool_levels[4]
    elif impressions > 5000:
        current_pool = pool_levels[3]
    elif impressions > 500:
        current_pool = pool_levels[2] if all_passed else pool_levels[1]
    elif impressions > 200:
        current_pool = pool_levels[1] if all_passed else pool_levels[0]

    # 生成突破建议
    breakthrough_actions = []
    if not checks["ctr"]["passed"]:
        breakthrough_actions.extend([
            f"🖼️ CTR仅{ctr}%（需≥8%）→ 封面图+标题是核心瓶颈",
            "📌 标题加数字和痛点词：「5个关键词」比「分享关键词」CTR高40%",
            "🎨 封面用3:4竖版，画作占80%+大号粗体标题文字",
            "📱 发完后用另一台手机看信息流缩略图效果，文字看不清就返工",
        ])
    if not checks["engagement_rate"]["passed"]:
        breakthrough_actions.extend([
            f"💬 互动率仅{eng_rate}%（需≥5%）→ 内容价值或互动引导不足",
            "❓ 文末必须有互动问题（算法检测到有问题句式会提升推荐）",
            "📝 发布后5分钟内在评论区自己留1条（≥15字）补充信息",
            "⭐ 增加可收藏的干货：Prompt分享、画家清单、参数设置",
        ])
    if checks["completion_rate"]["passed"] is not None and not checks["completion_rate"]["passed"]:
        breakthrough_actions.extend([
            f"📖 完读率仅{completion}%（需≥45%）→ 内容没留住用户",
            "🔥 前3句话必须制造悬念/冲突/好奇心，不能平铺直叙",
            "📐 正文用emoji分段+短句+小标题，增加阅读节奏感",
            "🖼️ 图文笔记确保每张图都有信息量，不要放凑数的图",
        ])

    return {
        "checks": checks,
        "all_passed": all_passed,
        "passed_count": passed_count,
        "total_checks": total_checks,
        "current_pool": current_pool,
        "can_breakthrough": all_passed,
        "breakthrough_actions": breakthrough_actions,
    }
