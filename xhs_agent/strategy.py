"""小红书运营Agent - 策略引擎（名画故事·油画审美 专属版）"""

import datetime
from .config import BEST_POSTING_TIMES, GROWTH_STAGES, CONTENT_TYPES


def _safe_load_tracker_analytics():
    """读取 tracker 最新统计与历史洞察；文件缺失或异常时安全降级。"""
    try:
        from .tracker import (
            get_overall_stats,
            extract_historical_insights,
            get_latest_operations_snapshot,
            get_adaptive_tool_profile,
        )

        return (
            get_overall_stats(),
            extract_historical_insights(),
            get_latest_operations_snapshot(),
            get_adaptive_tool_profile(),
        )
    except Exception:
        return (
            {
                "total_posts": 0,
                "tracked_posts": 0,
                "avg_views": 0,
                "avg_likes": 0,
                "avg_saves": 0,
                "avg_comments": 0,
                "avg_shares": 0,
                "total_views": 0,
                "total_shares": 0,
                "total_likes": 0,
                "total_saves": 0,
                "total_comments": 0,
                "avg_like_rate": 0.0,
                "avg_save_rate": 0.0,
                "avg_comment_rate": 0.0,
            },
            {"has_data": False},
            {},
            {},
        )


def _build_snapshot_execution_brief(snapshot: dict) -> dict:
    """根据最新运营面板快照生成今日执行建议。"""
    if not snapshot:
        return {
            "has_data": False,
            "note": "",
            "tool_focus": [],
            "execution_focus": [],
        }

    metrics = snapshot.get("metrics", {})
    views = int(metrics.get("views") or 0)
    follower_views = int(metrics.get("viewer_followers") or 0)
    avg_watch_seconds = float(metrics.get("avg_watch_seconds") or 0)
    conversion_rate = float(metrics.get("conversion_rate") or 0)
    sources = snapshot.get("traffic_sources") or []
    primary_source = sources[0] if sources else {}
    primary_source_name = primary_source.get("name", "")
    primary_source_percent = float(primary_source.get("percent") or 0)
    search_percent = next((float(item.get("percent") or 0) for item in sources if item.get("name") == "搜索"), 0.0)
    homepage_percent = next((float(item.get("percent") or 0) for item in sources if item.get("name") == "个人主页"), 0.0)
    follower_ratio = round((follower_views / views * 100.0), 1) if views > 0 else 0.0
    time_info = snapshot.get("viewer_time") or {}
    peak_window = time_info.get("peak_window", "晚间")
    peak_hour_label = time_info.get("peak_hour_label", "")

    note_parts = []
    if views:
        note_parts.append(f"最新运营面板显示统计期内观看总数约{views:,}")
    if primary_source_name:
        note_parts.append(f"{primary_source_name}贡献{primary_source_percent:.0f}%流量")
    if follower_ratio:
        note_parts.append(f"粉丝观看占比约{follower_ratio}%")
    if avg_watch_seconds:
        note_parts.append(f"平均观看时长约{avg_watch_seconds:.0f}秒")
    if conversion_rate <= 0:
        note_parts.append("当前转化仍未起量，今日目标应先放在公域承接和互动转化")

    tool_focus = []
    execution_focus = []

    if primary_source_percent >= 70:
        tool_focus.append(
            {
                "name": "封面工坊",
                "reason": f"{primary_source_name}占比高，说明公域推荐已经打开，接下来要继续稳住点击效率",
                "action": "封面保留大字强钩子和高反差首图，优先做一版能在瀑布流里一眼看懂的缩略图",
            }
        )
        execution_focus.append(f"今天优先在{peak_window}{f'（{peak_hour_label}）' if peak_hour_label else ''}发布，集中承接首页推荐流量")

    if search_percent < 10:
        tool_focus.append(
            {
                "name": "预发布检查",
                "reason": "搜索来源偏低，说明标题关键词和搜索承接还不够",
                "action": "标题补足「名画 / 油画 / 画家 / 色彩 / 提示词」等明确搜索词，避免只有情绪表达没有检索词",
            }
        )
        execution_focus.append("标题里至少保留1-2个可搜索关键词，正文前两段重复一次核心词，补搜索入口")

    if homepage_percent < 5 or follower_ratio < 15:
        tool_focus.append(
            {
                "name": "主页承接",
                "reason": "主页与粉丝承接偏弱，说明公域流量还没充分沉淀成长期资产",
                "action": "文末加关注引导，并在正文或评论区提醒读者去主页看同系列内容",
            }
        )
        execution_focus.append("正文结尾加一句“想看同系列内容可以进主页继续翻”，把首页流量导向主页和关注")

    if conversion_rate <= 0:
        tool_focus.append(
            {
                "name": "互动话术/组件",
                "reason": "转化率为0时不适合硬推成交，先把评论和收藏做起来更稳",
                "action": "结尾放低门槛互动问题，发布后5分钟内自留首评，引导评论和收藏而不是直接卖货",
            }
        )
        execution_focus.append("评论区首条放“你更想看哪类内容/哪位画家”的问题，把今日目标定成互动抬权重")

    if avg_watch_seconds and avg_watch_seconds < 25:
        execution_focus.append("前三句改成更短更狠的悬念句，尽量在第一屏完成钩子，先把停留再往上拉")

    return {
        "has_data": bool(note_parts),
        "note": "；".join(note_parts) + "。",
        "tool_focus": tool_focus[:5],
        "execution_focus": execution_focus[:4],
    }


def get_data_driven_execution_brief() -> dict:
    """
    基于 tracker 最新数据的执行摘要（工具优先级 + 执行重点）。
    无数据时返回引导先完成追踪的兜底内容。
    """
    stats, insights, snapshot, adaptive_profile = _safe_load_tracker_analytics()
    tracked = int(stats.get("tracked_posts") or 0)
    avg_views = int(stats.get("avg_views") or 0)
    total_views = int(stats.get("total_views") or 0)
    like_r = float(stats.get("avg_like_rate") or 0)
    save_r = float(stats.get("avg_save_rate") or 0)
    comment_r = float(stats.get("avg_comment_rate") or 0)
    total_shares = int(stats.get("total_shares") or 0)
    share_r = (total_shares / total_views * 100.0) if total_views > 0 else 0.0

    has_data = tracked > 0 and avg_views > 0
    snapshot_brief = _build_snapshot_execution_brief(snapshot)

    if not has_data and snapshot_brief.get("has_data"):
        result = snapshot_brief
        if adaptive_profile.get("weekly_update_note"):
            result["note"] = f"{adaptive_profile['weekly_update_note']} {result['note']}".strip()
        return result

    if not has_data:
        return {
            "has_data": False,
            "note": adaptive_profile.get("weekly_update_note") or "暂无有效追踪数据。请先在「数据复盘/笔记追踪」录入至少一篇笔记的浏览与互动，再解锁定向优化。",
            "tool_focus": [
                {
                    "name": "数据追踪",
                    "reason": "没有基准数据无法判断该优化曝光还是互动",
                    "action": "发布后在创作者中心记录浏览、赞、藏、评、分享各一项",
                },
            ],
            "execution_focus": [
                "今日发内容前，先打开追踪表准备回填字段",
                "首篇数据录入后，明天再看工具优先级是否变化",
            ],
        }

    tool_focus = []
    execution_focus = []
    note_parts = []

    # 互动尚可但曝光不足 → 优先 CTR / 分发侧
    views_low = avg_views < 450
    engagement_ok = like_r >= 3.0 and save_r >= 2.5
    if views_low and engagement_ok:
        note_parts.append("赞藏不错但曝光偏低，优先拉CTR与分发")
        tool_focus.extend(
            [
                {
                    "name": "封面工坊",
                    "reason": "曝光不足时首图点击率往往是瓶颈",
                    "action": "做2版封面：强标题大字+高对比，选更吸睛的一版再发",
                },
                {
                    "name": "预发布检查",
                    "reason": "标题与首帧决定用户是否点进来",
                    "action": "检查标题是否有悬念/反差；首图是否在缩略图下仍清晰",
                },
                {
                    "name": "流量池自检",
                    "reason": "确认话题与标签是否过窄或重复踩雷",
                    "action": "补充1–2个泛话题标签，避免只打极冷门词",
                },
            ]
        )
        execution_focus.extend(
            [
                "发布前用同一文案试两版封面，12小时后再看点击率倾向",
                "首图底部留大白字区，保证手机瀑布流里标题可读",
            ]
        )

    if comment_r < 1.0:
        note_parts.append("评论率偏低，需加强互动设计")
        tool_focus.append(
            {
                "name": "互动话术/组件",
                "reason": "评论率低多因缺少「接得住的话题」",
                "action": "文末抛二选一或轻争议问题；发后5分钟内自留第一条神评论",
            }
        )
        execution_focus.append("今日正文结尾加一句「你站哪边？」类互动句，并准时蹲评论")

    if share_r < 0.5:
        note_parts.append("分享率偏低，可加强社交货币与利他感")
        tool_focus.append(
            {
                "name": "合集与利他结构",
                "reason": "分享常来自「值得转给好友」的清单或金句",
                "action": "加一段可截图的清单/金句；选题偏盘点、对比、冷知识",
            }
        )
        execution_focus.append("加一句「转给同好」式结尾，或做一张可保存的清单图")

    # 有数据但上述问题不突出：用历史洞察兜底
    if not note_parts:
        best_ct = insights.get("best_content_type")
        best_t = insights.get("best_posting_time")
        note = (
            f"近{tracked}篇有数据，均浏览约{avg_views}。"
            + (f"历史表现较好类型：「{best_ct}」。" if best_ct else "")
            + "建议稳住节奏并做小步试错。"
        )
        tool_focus = [
            {
                "name": "内容日历",
                "reason": "数据平稳时优先保发布节奏与系列感",
                "action": "固定发文窗口，系列选题至少连更2篇再评估",
            }
        ]
        execution_focus = [
            "复盘数据最好的一篇，复用其标题结构与封面版式",
            "预留20分钟集中回复评论以抬高互动权重",
        ]
        if best_t:
            execution_focus.append(f"优先在{best_t}前后发布，贴合历史高光时段")
        if insights.get("discovered_patterns"):
            execution_focus.append(insights["discovered_patterns"][0][:80])
        result = {
            "has_data": True,
            "note": note,
            "tool_focus": tool_focus[:5],
            "execution_focus": execution_focus[:4],
        }
        if snapshot_brief.get("has_data"):
            result["note"] = f"{snapshot_brief['note']} {result['note']}".strip()
            result["tool_focus"] = (snapshot_brief.get("tool_focus") or []) + result["tool_focus"]
            result["execution_focus"] = (snapshot_brief.get("execution_focus") or []) + result["execution_focus"]
        return {
            "has_data": result["has_data"],
            "note": result["note"],
            "tool_focus": result["tool_focus"][:5],
            "execution_focus": result["execution_focus"][:4],
        }

    note = "；".join(note_parts) + "。"
    # 去重工具名（保留顺序）
    seen = set()
    unique_tools = []
    for t in tool_focus:
        name = t.get("name", "")
        if name and name not in seen:
            seen.add(name)
            unique_tools.append(t)
    result = {
        "has_data": True,
        "note": note,
        "tool_focus": unique_tools[:5],
        "execution_focus": execution_focus[:4],
    }
    if snapshot_brief.get("has_data"):
        result["note"] = f"{snapshot_brief['note']} {result['note']}".strip()
        result["tool_focus"] = (snapshot_brief.get("tool_focus") or []) + result["tool_focus"]
        result["execution_focus"] = (snapshot_brief.get("execution_focus") or []) + result["execution_focus"]
        # 工具按名称去重
        deduped_tools = []
        seen_names = set()
        for item in result["tool_focus"]:
            name = item.get("name", "")
            if name and name not in seen_names:
                seen_names.add(name)
                deduped_tools.append(item)
        result["tool_focus"] = deduped_tools[:5]
    if adaptive_profile.get("weekly_update_note"):
        result["note"] = f"{adaptive_profile['weekly_update_note']} {result['note']}".strip()
    for line in (adaptive_profile.get("weekly_actions") or [])[:2]:
        if line and line not in result["execution_focus"]:
            result["execution_focus"].append(line)
    return {
        "has_data": result["has_data"],
        "note": result["note"],
        "tool_focus": result["tool_focus"][:5],
        "execution_focus": result["execution_focus"][:4],
    }


def get_current_stage(follower_count: int) -> dict:
    """根据当前粉丝数判断所处阶段，返回对应策略"""
    if follower_count < 1000:
        stage_name = "冷启动期"
    elif follower_count < 10000:
        stage_name = "成长期"
    elif follower_count < 100000:
        stage_name = "爆发期"
    else:
        stage_name = "稳定期"

    stage_info = GROWTH_STAGES[stage_name]
    return {"stage": stage_name, **stage_info}


def get_today_posting_times() -> list:
    """获取今天推荐的发布时间"""
    today = datetime.datetime.now()
    is_weekend = today.weekday() >= 5
    key = "weekend" if is_weekend else "weekday"
    times = BEST_POSTING_TIMES[key]
    return sorted(times, key=lambda x: x["score"], reverse=True)


def get_weekly_plan(category: str, follower_count: int) -> list:
    """生成一周的运营计划（艺术账号专属排期）"""
    stage = get_current_stage(follower_count)
    stage_name = stage["stage"]
    try:
        from .tracker import get_adaptive_tool_profile
        adaptive_profile = get_adaptive_tool_profile()
    except Exception:
        adaptive_profile = {}

    # 艺术账号的发布节奏（不宜太密，每篇要保证图片质量）
    if stage_name == "冷启动期":
        posts_per_day = {0: 2, 1: 1, 2: 2, 3: 1, 4: 2, 5: 1, 6: 1}
    elif stage_name == "成长期":
        posts_per_day = {0: 1, 1: 2, 2: 1, 3: 2, 4: 1, 5: 1, 6: 1}
    else:
        posts_per_day = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0}

    # 为一周安排不同的内容类型组合（确保多样性）
    weekly_content_rotation = [
        # 周一：AI创作 + 画家赏析（新一周用新鲜内容开场）
        ["AI油画创作过程", "画家作品赏析"],
        # 周二：色彩解析（干货日）
        ["色彩/构图解析"],
        # 周三：AI对比 + 教程（话题性+实用性）
        ["AI vs 真实油画对比", "AI绘画教程"],
        # 周四：画家故事（故事日）
        ["画家故事/八卦"],
        # 周五：合集 + AI创作（冲数据日）
        ["艺术清单合集", "AI油画创作过程"],
        # 周六：轻松赏析（周末轻内容）
        ["画家作品赏析"],
        # 周日：展览/总结
        ["展览/拍卖资讯"],
    ]

    focus = adaptive_profile.get("content_focus") or {}
    primary_type = focus.get("primary_type")
    secondary_type = focus.get("secondary_type")
    weak_type = focus.get("weak_type")

    if primary_type in CONTENT_TYPES:
        weekly_content_rotation[0] = [primary_type]
        weekly_content_rotation[3] = [primary_type]
        weekly_content_rotation[4] = [primary_type, secondary_type] if secondary_type in CONTENT_TYPES and secondary_type != primary_type else [primary_type]
    if secondary_type in CONTENT_TYPES and secondary_type != primary_type:
        weekly_content_rotation[2] = [secondary_type]
        weekly_content_rotation[6] = [secondary_type]
    if weak_type in CONTENT_TYPES:
        replacement = primary_type if primary_type in CONTENT_TYPES else secondary_type
        if replacement in CONTENT_TYPES:
            weekly_content_rotation = [
                [replacement if item == weak_type else item for item in day_types]
                for day_types in weekly_content_rotation
            ]

    week_days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    today = datetime.datetime.now()
    start_of_week = today - datetime.timedelta(days=today.weekday())

    plan = []
    for day_offset in range(7):
        day_date = start_of_week + datetime.timedelta(days=day_offset)
        is_weekend = day_offset >= 5
        time_key = "weekend" if is_weekend else "weekday"
        best_times = sorted(
            BEST_POSTING_TIMES[time_key],
            key=lambda x: x["score"],
            reverse=True
        )

        num_posts = posts_per_day.get(day_offset, 1)
        day_types = weekly_content_rotation[day_offset]

        day_plan = {
            "day": week_days[day_offset],
            "date": day_date.strftime("%m月%d日"),
            "posts": []
        }

        for i in range(num_posts):
            content_type = day_types[i % len(day_types)]
            post_time = best_times[i % len(best_times)]

            day_plan["posts"].append({
                "time": post_time["time"].split("-")[0],
                "content_type": content_type,
                "category": category,
                "time_reason": post_time["desc"],
                "type_info": CONTENT_TYPES[content_type],
                "topic_hint": _get_topic_hint(content_type, day_offset),
            })

        day_plan["daily_tasks"] = _get_daily_tasks(stage_name, day_offset)
        if adaptive_profile.get("weekly_update_note"):
            day_plan["adaptive_note"] = adaptive_profile.get("weekly_update_note")
        plan.append(day_plan)

    return plan


def _get_topic_hint(content_type: str, day_of_week: int) -> str:
    """为每天的内容类型提供选题提示"""
    hints = {
        "AI油画创作过程": [
            "尝试用AI模仿一位当代画家的风格",
            "用AI画一组季节主题的油画",
            "挑战用AI生成超写实油画",
            "AI学习抽象表现主义",
            "用AI重现经典名画",
            "尝试混合多种画派风格",
            "AI油画中的东方美学",
        ],
        "画家作品赏析": [
            "挖掘名画背后的细思极恐/隐藏细节（悬念感）",
            "某位画家最颠覆常理/最贵的一幅画（金钱反差）",
            "一幅看似普通的画，其实大有来头（冷知识解密）",
            "画家不为人知的特殊癖好与作品关系（八卦猎奇）",
            "介绍一位冷门但经历传奇的当代画家（故事性）",
        ],
        "AI vs 真实油画对比": [
            "选一位画家的代表作，用AI复刻",
            "同一构图的AI版 vs 手绘版",
            "AI能学会油画的肌理感吗？",
        ],
        "色彩/构图解析": [
            "拆解一幅画的色彩关系",
            "画面中的黄金比例",
            "冷暖色调的情绪表达",
        ],
        "画家故事/八卦": [
            "讲一个画家从落魄到成名的故事",
            "画家之间的恩怨情仇",
            "一幅画背后的真实故事",
        ],
        "艺术清单合集": [
            "「值得收藏的10幅当代油画」",
            "「5位你不能不知道的当代女性画家」",
            "「用AI生成的最美油画TOP10」",
        ],
        "AI绘画教程": [
            "从零开始用AI画一幅油画",
            "5个提示词技巧让AI油画更专业",
            "如何让AI理解油画的笔触感",
        ],
        "展览/拍卖资讯": [
            "近期海外重要艺术展览盘点",
            "本周拍卖场上的天价油画",
            "值得关注的线上艺术展",
        ],
    }
    type_hints = hints.get(content_type, ["自由发挥"])
    return type_hints[day_of_week % len(type_hints)]


def _get_daily_tasks(stage_name: str, day_of_week: int) -> list:
    """根据阶段和星期生成每日任务（艺术账号专属）"""
    base_tasks = [
        "🎨 浏览小红书「当代艺术/油画/AI绘画」热门笔记 15分钟",
        "💬 回复所有新评论和私信（艺术讨论要有深度）",
        "👀 检查昨日笔记数据（浏览/点赞/收藏/评论）",
    ]

    if stage_name == "冷启动期":
        base_tasks.extend([
            "🔍 收集3-5张高清画作素材（注意版权）",
            "📝 研究1个海外当代画家，为下一篇笔记积累素材",
            "🤝 在 #当代艺术 #油画 话题下评论5-8条（留专业见解）",
            "🖼️ 用AI生成1-2张油画作品，积累素材库",
        ])
    elif stage_name == "成长期":
        base_tasks.extend([
            "📊 分析本周哪类内容（画家/AI创作/教程）数据最好",
            "🎯 优化个人简介：突出「AI油画」和「当代艺术」标签",
            "🤝 找2个艺术/设计类同量级博主互动",
            "💡 关注1个海外艺术资讯源（Artsy/Artnet等）",
        ])
    elif stage_name == "爆发期":
        base_tasks.extend([
            "📈 关注本周艺术圈热点（展览/拍卖/事件）",
            "🤝 维护粉丝群，策划一次艺术讨论话题",
            "💡 策划下一个系列内容（如「10位改变当代艺术的画家」）",
        ])

    # 周末特殊任务
    if day_of_week >= 5:
        base_tasks.append("📋 复盘本周数据：哪些画家/风格最受欢迎？")
        base_tasks.append("🖼️ 批量制作下周的封面图和AI油画素材")

    # 每周三：素材日
    if day_of_week == 2:
        base_tasks.append("🔄 更新AI油画素材库 + 收集海外画家新动态")

    # 每周五：蹭热点
    if day_of_week == 4:
        base_tasks.append("🔥 检查是否有可蹭的艺术热点话题")

    # 数据驱动的 1–2 条动态任务（无数据或异常时静默跳过）
    try:
        brief = get_data_driven_execution_brief()
        for line in (brief.get("execution_focus") or [])[:2]:
            if line:
                base_tasks.append(f"📊（数据建议）{line}")
    except Exception:
        pass

    return base_tasks


def get_optimization_tips(metrics: dict) -> list:
    """根据数据指标给出优化建议（艺术账号专属）"""
    tips = []
    views = metrics.get("views", 0)
    likes = metrics.get("likes", 0)
    saves = metrics.get("saves", 0)
    comments = metrics.get("comments", 0)
    shares = metrics.get("shares", 0)

    if views == 0:
        return ["📌 暂无数据，请先发布内容并记录数据后再来分析"]

    # 点赞率分析
    like_rate = (likes / views) * 100 if views > 0 else 0
    if like_rate < 3:
        tips.append({
            "metric": "点赞率",
            "value": f"{like_rate:.1f}%",
            "status": "偏低",
            "advice": [
                "🎨 封面不要只放纯画作，必须加上大字标题制造悬念或反差！",
                "💡 不要只做美的搬运工，要提供「信息增量」或「冷知识故事」",
                "📝 文末加引导：「如果是你，你会花3亿买这幅画吗？」",
                "🔥 尝试更有冲击力的标题：用惊叹/常理反差/金钱数字增加点击欲",
            ]
        })
    elif like_rate >= 5:
        tips.append({
            "metric": "点赞率",
            "value": f"{like_rate:.1f}%",
            "status": "优秀",
            "advice": ["🎉 审美共鸣做得很好！继续保持这种风格和选题方向"]
        })

    # 收藏率分析
    save_rate = (saves / views) * 100 if views > 0 else 0
    if save_rate < 3:
        tips.append({
            "metric": "收藏率",
            "value": f"{save_rate:.1f}%",
            "status": "偏低",
            "advice": [
                "📚 增加故事密度：把画作当成引子，讲一个引人入胜的冷门故事",
                "📋 多做盘点/猎奇类合集：「这5幅被禁止展出的名画背后」",
                "🎯 提供社交货币：让读者觉得知道这个故事很酷，值得收藏作为谈资",
                "💾 文末引导：「先收藏🌟 以后去美术馆装杯用」",
            ]
        })
    elif save_rate >= 8:
        tips.append({
            "metric": "收藏率",
            "value": f"{save_rate:.1f}%",
            "status": "优秀",
            "advice": ["🌟 内容价值感很强！艺术干货类路线很适合你"]
        })

    # 评论率分析
    comment_rate = (comments / views) * 100 if views > 0 else 0
    if comment_rate < 1:
        tips.append({
            "metric": "评论率",
            "value": f"{comment_rate:.1f}%",
            "status": "偏低",
            "advice": [
                "❓ 文末抛出讨论话题：「你觉得AI画的能算艺术吗？」",
                "🗳️ 做对比投票：展示两幅画，问粉丝更喜欢哪一幅",
                "💬 自己在评论区先抛观点，带动讨论氛围",
                "🎨 分享有争议性的艺术观点，激发讨论",
                "📢 回复每一条评论，给评论者被重视的感觉",
            ]
        })
    elif comment_rate >= 2:
        tips.append({
            "metric": "评论率",
            "value": f"{comment_rate:.1f}%",
            "status": "优秀",
            "advice": ["🗣️ 互动氛围非常好！你的内容引发了共鸣和讨论"]
        })

    # 分享率分析
    share_rate = (shares / views) * 100 if views > 0 else 0
    if share_rate < 0.5:
        tips.append({
            "metric": "分享率",
            "value": f"{share_rate:.1f}%",
            "status": "偏低",
            "advice": [
                "🎁 创作更多「社交货币」型内容——让人想转发给朋友的",
                "📋 合集类/盘点类内容更容易被分享（如「最美10幅油画」）",
                "🤯 制造惊喜感：AI画的太像真画了！让人忍不住分享",
            ]
        })

    # 浏览量分析
    if views < 300:
        tips.append({
            "metric": "浏览量",
            "value": str(views),
            "status": "偏低",
            "advice": [
                "📌 标题是否太文艺平淡？必须要抛出问题/制造悬念（如金钱、反常理）",
                "🖼️ 封面上必须要有大字文案！纯画作无法在瀑布流里竞争点击率",
                "⏰ 建议改在晚间高峰期 19:00 - 21:30 发布",
                "🏷️ 标签不仅要有大类，还要加一些猎奇、故事、揭秘类的泛泛标签",
                "🔥 尝试切入更有争议或带有戏剧性色彩的艺术家故事",
            ]
        })

    return tips


def get_title_formulas() -> list:
    """返回爆款标题公式（名画故事·油画审美专属）"""
    return [
        {
            "formula": "反常理/金钱对比 + 悬念/质疑",
            "example": "他把照片画模糊居然卖了3亿💰｜凭什么这么贵",
            "适用": "画家故事/八卦、画家作品赏析"
        },
        {
            "formula": "细节放大 + 细思极恐/隐藏秘密",
            "example": "这幅挂在卢浮宫角落的画，放大后细思极恐🤫",
            "适用": "画家作品赏析"
        },
        {
            "formula": "冷知识 + 打破认知",
            "example": "被骗了100年！原来梵高晚年根本不是疯子🤯",
            "适用": "画家故事/八卦"
        },
        {
            "formula": "数字 + 猎奇盘点 + 社交货币",
            "example": "5幅曾被禁止展出的世界名画，第一幅就让人脸红",
            "适用": "艺术清单合集"
        },
        {
            "formula": "AI vs 真实 + 颠覆认知",
            "example": "我让AI重画了《蒙娜丽莎》，结果美术系教授看呆了",
            "适用": "AI vs 真实油画对比"
        },
        {
            "formula": "低门槛代入 + 艺术装杯指南",
            "example": "去美术馆怎么装作很懂画？记住这3个万能话术",
            "适用": "艺术科普"
        },
    ]


def get_hashtag_strategy(category: str) -> dict:
    """根据内容类别返回标签使用策略（艺术领域专属）"""
    # 针对不同内容分类推荐不同的标签组合
    tag_pools = {
        "AI油画创作": {
            "大流量": ["#AI绘画", "#油画"],
            "中等": ["#AI油画", "#Midjourney", "#AI艺术"],
            "长尾": ["#AI油画教程", "#AI画画", "#AI绘画提示词"],
        },
        "海外当代画家": {
            "大流量": ["#当代艺术", "#油画"],
            "中等": ["#画家", "#艺术作品", "#西方油画"],
            "长尾": ["#当代油画家", "#海外艺术", "#艺术科普"],
        },
        "default": {
            "大流量": ["#油画", "#艺术"],
            "中等": ["#当代艺术", "#AI绘画", "#画作赏析"],
            "长尾": ["#艺术分享", "#画家推荐", "#油画欣赏"],
        }
    }

    pool = tag_pools.get(category, tag_pools["default"])

    return {
        "总数建议": "每篇笔记使用 8-12 个标签，艺术类标签竞争相对小，容易获得曝光",
        "标签分层": {
            "大流量标签(2-3个)": f"如 {' '.join(pool['大流量'])} 等百万级话题，拉曝光",
            "中等标签(3-4个)": f"如 {' '.join(pool['中等'])} 等垂直领域标签",
            "长尾标签(2-3个)": f"如 {' '.join(pool['长尾'])} 等精准匹配标签",
            "品牌/IP标签(1个)": "如 #我的AI油画日记 等个人专属标签",
        },
        "注意事项": [
            "艺术类标签竞争度低于美妆/穿搭，更容易进入热门",
            "画家名字可以作为长尾标签（如 #GerhardRichter）",
            "AI相关标签近期热度上升，是流量红利期",
            "跟随官方活动标签（如 #我的艺术日记 等）",
            "中英文标签都要用，覆盖更多搜索词",
        ]
    }
