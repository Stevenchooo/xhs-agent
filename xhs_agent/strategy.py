"""小红书运营Agent - 策略引擎（AI油画·当代艺术 专属版）"""

import datetime
from .config import BEST_POSTING_TIMES, GROWTH_STAGES, CONTENT_TYPES


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
            "介绍一位冷门但实力强的当代画家",
            "某位画家的风格演变历程",
            "同主题不同画家的表现对比",
            "年轻一代当代画家推荐",
            "该画家最被低估的一幅作品",
            "从色彩角度赏析画家作品",
            "画家的成名之路",
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
                "🎨 封面图不够吸引人——艺术号封面是第一生命力，用高饱和度画作",
                "💡 加入更多个人观点和情感表达，不要只做搬运",
                "📝 文末加引导：「被这幅画打动的话，给我一个❤️」",
                "🔥 尝试更有冲击力的标题：用惊叹/反差/数字增加点击欲",
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
                "📚 增加干货密度：画家介绍要有知识增量，不能太浅",
                "📋 多做合集类内容：「10幅值得收藏的当代油画」收藏率极高",
                "🎯 加入可操作的内容：AI提示词分享、色彩分析、配色方案",
                "💾 文末引导：「先收藏🌟 以后慢慢看」",
                "🖼️ 高清大图本身就有收藏价值，确保图片质量过硬",
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
                "📌 检查标题是否包含热门关键词（油画/当代艺术/AI绘画）",
                "🖼️ 封面图是否足够抓眼球（艺术号封面要极致美感）",
                "⏰ 发布时间是否在21:00-23:00黄金时段？",
                "🏷️ 标签是否精准？建议同时用大标签+长尾标签",
                "🔥 尝试蹭热点：艺术展览/拍卖新闻/AI绘画工具更新",
            ]
        })

    return tips


def get_title_formulas() -> list:
    """返回爆款标题公式（AI油画·当代艺术专属）"""
    return [
        {
            "formula": "画家名 + 惊叹/反差",
            "example": "Gerhard Richter｜把照片画模糊居然卖了3亿",
            "适用": "画家作品赏析"
        },
        {
            "formula": "数字 + 合集 + 情感钩子",
            "example": "10幅让你看一眼就沉默的当代油画",
            "适用": "艺术清单合集"
        },
        {
            "formula": "AI vs 手绘 + 悬念",
            "example": "我让AI模仿莫奈画了100次｜结果你猜怎样",
            "适用": "AI vs 真实油画对比"
        },
        {
            "formula": "干货标记 + 主题 + 适用人群",
            "example": "保姆级｜用Midjourney生成油画风作品全教程",
            "适用": "AI绘画教程"
        },
        {
            "formula": "疑问句 + 颠覆认知",
            "example": "为什么这幅「看不懂」的画能值9000万美元？",
            "适用": "画家故事/八卦"
        },
        {
            "formula": "色彩/感官 + 情绪表达",
            "example": "这组蓝色油画，看完整个人都安静下来了",
            "适用": "色彩/构图解析"
        },
        {
            "formula": "时间线 + 变化/成长",
            "example": "用AI画油画30天｜从翻车到惊艳的全过程",
            "适用": "AI油画创作过程"
        },
        {
            "formula": "推荐语气 + 冷门发现",
            "example": "求你们看看这个宝藏画家｜每一幅都是神作",
            "适用": "海外当代画家推荐"
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
