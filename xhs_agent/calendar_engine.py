"""小红书运营Agent - 日历智能引擎
根据星期几、节日节气、季节、热点、官方活动自动匹配最佳选题、时间和内容
"""

import datetime

# ==================== 中国节日/节气/纪念日 + 艺术关联 ====================
CALENDAR_EVENTS = {
    # 格式：(月, 日): {名称, 艺术角度, 选题方向, 热度}
    # --- 重要节日 ---
    (1, 1): {"name": "元旦", "art_angle": "新年主题AI油画合集", "topic": "用AI画了9幅「新生」主题油画🎨｜新年第一组作品", "heat": "★★★★"},
    (2, 14): {"name": "情人节", "art_angle": "爱情主题名画", "topic": "艺术史上最动人的10幅爱情油画💕｜哪幅打动了你", "heat": "★★★★★"},
    (3, 8): {"name": "妇女节/女神节", "art_angle": "女性画家专题", "topic": "5位改变艺术史的女性画家🌹｜每一位都是传奇", "heat": "★★★★★"},
    (3, 12): {"name": "植树节", "art_angle": "树木/自然主题油画", "topic": "油画里的树有多美🌳｜从莫奈到Hockney的森林", "heat": "★★"},
    (3, 21): {"name": "春分", "art_angle": "春天色彩主题", "topic": "用AI画了一组「春天的颜色」🌸｜印象派配色太治愈了", "heat": "★★★"},
    (4, 5): {"name": "清明节", "art_angle": "中国山水与西方风景画对比", "topic": "中国山水画vs西方风景油画🏔️｜同样画山水 为什么感觉完全不同", "heat": "★★★"},
    (4, 22): {"name": "世界地球日", "art_angle": "自然/环保主题艺术", "topic": "这些画家用油画为地球发声🌍｜看完想保护环境", "heat": "★★★"},
    (5, 1): {"name": "劳动节", "art_angle": "画家的「劳动」——工作室日常", "topic": "当代画家一天怎么过？｜7位大师的工作室大揭秘🎨", "heat": "★★★"},
    (5, 18): {"name": "国际博物馆日", "art_angle": "博物馆名画专题", "topic": "全球10个必去的油画博物馆🏛️｜收藏这篇等出发", "heat": "★★★★★"},
    (5, 20): {"name": "520", "art_angle": "爱情主题画作", "topic": "画家们怎么画爱情💗｜从Klimt的吻到Hockney的泳池", "heat": "★★★★"},
    (6, 1): {"name": "儿童节", "art_angle": "童趣/童年主题", "topic": "用AI画了一组「回到童年」的油画🧸｜第5张我哭了", "heat": "★★★"},
    (6, 21): {"name": "夏至", "art_angle": "夏日色彩", "topic": "油画里的夏天有多美☀️｜这组色彩看完整个人都温暖了", "heat": "★★★"},
    (8, 8): {"name": "立秋", "art_angle": "秋色主题", "topic": "为什么秋天是油画最美的季节🍂｜从莫奈到AI的秋色", "heat": "★★★"},
    (9, 10): {"name": "教师节", "art_angle": "艺术教育/大师的老师", "topic": "每个大师背后都有一位老师👨‍🏫｜画家师徒关系有多狠", "heat": "★★★"},
    (10, 1): {"name": "国庆节", "art_angle": "中国元素AI油画", "topic": "用AI画了一组「东方美」油画🏮｜当代艺术的中国表达", "heat": "★★★★"},
    (10, 31): {"name": "万圣节", "art_angle": "暗黑/哥特风油画", "topic": "艺术史上最「可怕」的10幅画🎃｜万圣节特辑", "heat": "★★★★"},
    (11, 11): {"name": "双十一", "art_angle": "艺术品收藏入门", "topic": "双11不如买幅画💰｜普通人能买得起的当代艺术入门指南", "heat": "★★★★"},
    (12, 21): {"name": "冬至", "art_angle": "冬日/雪景油画", "topic": "油画里的雪为什么这么美❄️｜从莫奈到AI的冬日", "heat": "★★★"},
    (12, 24): {"name": "平安夜", "art_angle": "节日氛围AI油画", "topic": "用AI画了一组「平安夜」油画🎄｜暖到想哭", "heat": "★★★★"},
    (12, 25): {"name": "圣诞节", "art_angle": "西方宗教画/节日艺术", "topic": "圣诞节在油画里长什么样🎅｜从文艺复兴到当代", "heat": "★★★★"},

    # --- 艺术界重要日子 ---
    (3, 14): {"name": "π日/白色情人节", "art_angle": "数学与艺术", "topic": "油画里藏着多少数学秘密📐｜黄金比例的艺术", "heat": "★★★"},
    (4, 15): {"name": "世界艺术日", "art_angle": "达芬奇诞辰", "topic": "今天是世界艺术日🎨｜AI能成为下一个达芬奇吗", "heat": "★★★★★"},
    (7, 29): {"name": "梵高去世纪念日", "art_angle": "梵高专题", "topic": "如果梵高活到今天会用AI画画吗🌻｜7月29日特别篇", "heat": "★★★★"},
}

# ==================== 官方活动（参与送流量加持） ====================
# 格式：每个活动包含名称、话题标签、起止日期、艺术角度、内容建议
OFFICIAL_ACTIVITIES = [
    {
        "name": "我想和你交换春天",
        "hashtag": "#交换春天",
        "start": (3, 10),   # 开始日期 (月, 日)
        "end": (4, 30),     # 结束日期 (月, 日)
        "benefit": "发春天赢流量",
        "heat": "★★★★★",
        "art_angle": "春天主题AI油画·印象派春日",
        "topic": "用AI画了9个春天的瞬间🌸｜哪个是你的春天",
        "content_tips": [
            "结合活动主题「交换春天」，分享春天相关的AI油画创作",
            "内容可以是：春天的花园、城市樱花、菜场春菜、公园散步、夜游等日常春天瞬间",
            "印象派风格最适合春天主题：莫奈、雷诺阿的光影和色彩",
            "正文和标签必须带上 #交换春天 话题标签才能获得活动流量扶持",
            "活动期间可以多次参与，每周发1-2篇春天主题内容",
        ],
        "daily_package_index": 10,  # 对应 DAILY_PACKAGES 中的索引
    },
]


def get_active_official_activities() -> list:
    """获取当前正在进行的官方活动"""
    now = datetime.datetime.now()
    month, day = now.month, now.day
    active = []
    for act in OFFICIAL_ACTIVITIES:
        s_m, s_d = act["start"]
        e_m, e_d = act["end"]
        # 简单的日期范围判断（不跨年）
        start_num = s_m * 100 + s_d
        end_num = e_m * 100 + e_d
        today_num = month * 100 + day
        if start_num <= today_num <= end_num:
            active.append(act)
    return active


# ==================== 星期策略 ====================
WEEKDAY_STRATEGY = {
    0: {  # 周一
        "mood": "周一打工人状态：需要美感和能量",
        "best_time": "21:00",
        "best_types": ["AI油画合集", "色彩/构图解析"],
        "reason": "周一晚上人们需要视觉治愈，精美画作合集最受欢迎",
        "avoid": "不发长教程（周一没耐心看长内容）",
    },
    1: {  # 周二
        "mood": "进入工作节奏，开始有碎片时间",
        "best_time": "21:00",
        "best_types": ["画家作品赏析", "画家故事/八卦"],
        "reason": "周二用户更愿意消费知识型内容，画家故事完读率高",
        "avoid": "",
    },
    2: {  # 周三
        "mood": "一周的中间点，适合深度内容",
        "best_time": "12:00",
        "best_types": ["AI vs 真实油画对比", "AI绘画教程"],
        "reason": "周三午休时间是互动高峰，争议性内容（AI vs 真画）容易引发讨论",
        "avoid": "",
    },
    3: {  # 周四
        "mood": "快到周末了，想看轻松有趣的内容",
        "best_time": "21:00",
        "best_types": ["画家故事/八卦", "艺术清单合集"],
        "reason": "周四晚上用户心态放松，故事类和八卦类内容点赞率高",
        "avoid": "",
    },
    4: {  # 周五
        "mood": "TGIF心态，想看美的东西犒赏自己",
        "best_time": "18:30",
        "best_types": ["AI油画合集", "展览/拍卖资讯"],
        "reason": "周五下班后发精美合集，用户有心情欣赏。展览资讯适合周末前发（引导周末看展）",
        "avoid": "不发教程（周五没人想学东西）",
    },
    5: {  # 周六
        "mood": "周末慢节奏，愿意看深度长内容",
        "best_time": "10:00",
        "best_types": ["画家作品赏析", "色彩/构图解析", "AI绘画教程"],
        "reason": "周六上午用户有耐心看长图文，深度画家介绍和教程收藏率最高",
        "avoid": "",
    },
    6: {  # 周日
        "mood": "周末尾声，开始为下周储备",
        "best_time": "20:30",
        "best_types": ["艺术清单合集", "AI油画合集"],
        "reason": "周日晚上适合发合集/盘点类内容，用户会收藏留着下周看",
        "avoid": "不发太长的内容（周日晚上想早睡）",
    },
}

# ==================== 季节主题 ====================
SEASON_THEMES = {
    "spring": {  # 3-5月
        "colors": "嫩绿、樱花粉、丁香紫、鹅黄",
        "subjects": "花园、春雨、新芽、蝴蝶、晨光",
        "painters": "莫奈（花园系列）、Hockney（春天的约克郡）、梵高（杏花）",
        "ai_keywords": "spring garden, cherry blossom, fresh green, morning dew, Monet-inspired",
    },
    "summer": {  # 6-8月
        "colors": "海蓝、日落橙、热带绿、珊瑚红",
        "subjects": "海滩、泳池、日落、热带植物、冰饮",
        "painters": "Hockney（泳池系列）、Sorolla（海滩光影）、Gauguin（大溪地）",
        "ai_keywords": "summer beach, swimming pool, golden sunset, tropical, Hockney-inspired",
    },
    "autumn": {  # 9-11月
        "colors": "枫叶红、琥珀黄、焦糖棕、深紫",
        "subjects": "落叶、收获、暮色、壁炉、旧书",
        "painters": "Peter Doig（秋日风景）、Richter（秋天系列）、Klimt（金色）",
        "ai_keywords": "autumn leaves, golden hour, harvest, warm amber tones, melancholy beauty",
    },
    "winter": {  # 12-2月
        "colors": "雪白、冰蓝、暖灰、烛光黄",
        "subjects": "雪景、窗户、烛光、热饮、极光",
        "painters": "Monet（雪景）、Bruegel（冬日猎人）、Hammershøi（冬日室内）",
        "ai_keywords": "winter snow, candlelight, frosted window, cozy interior, cold blue and warm gold",
    },
}


def get_current_season() -> dict:
    """获取当前季节信息"""
    month = datetime.datetime.now().month
    if month in (3, 4, 5):
        return {**SEASON_THEMES["spring"], "name": "春天"}
    elif month in (6, 7, 8):
        return {**SEASON_THEMES["summer"], "name": "夏天"}
    elif month in (9, 10, 11):
        return {**SEASON_THEMES["autumn"], "name": "秋天"}
    else:
        return {**SEASON_THEMES["winter"], "name": "冬天"}


def get_nearby_events(days_range: int = 7) -> list:
    """获取未来N天内的节日/纪念日"""
    today = datetime.datetime.now()
    events = []
    for i in range(days_range):
        check_date = today + datetime.timedelta(days=i)
        key = (check_date.month, check_date.day)
        if key in CALENDAR_EVENTS:
            event = CALENDAR_EVENTS[key].copy()
            event["date"] = check_date.strftime("%m月%d日")
            event["days_away"] = i
            event["weekday"] = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][check_date.weekday()]
            events.append(event)
    return events


def get_smart_recommendation() -> dict:
    """根据今天的所有上下文信息，生成智能推荐"""
    now = datetime.datetime.now()
    weekday = now.weekday()
    month = now.month
    day = now.day
    date_str = now.strftime("%m月%d日")
    day_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][weekday]

    # 1. 获取星期策略
    week_strategy = WEEKDAY_STRATEGY[weekday]

    # 2. 检查今天是否有节日
    today_key = (month, day)
    today_event = CALENDAR_EVENTS.get(today_key)

    # 3. 获取季节
    season = get_current_season()

    # 4. 获取未来7天的节日（提前准备）
    upcoming = get_nearby_events(7)

    # 5. 综合判断
    result = {
        "date": date_str,
        "weekday": day_name,
        "season": season,
        "is_weekend": weekday >= 5,
    }

    # 如果今天是节日，优先蹭节日热点
    if today_event:
        result["priority"] = "holiday"
        result["recommended_type"] = "节日热点"
        result["recommended_topic"] = today_event["topic"]
        result["recommended_time"] = "10:00" if weekday >= 5 else "12:00"
        result["reason"] = f"今天是{today_event['name']}（热度{today_event['heat']}），蹭节日流量！节日内容的初始推荐量是平时的2-3倍"
        result["event"] = today_event
    else:
        # 没有节日，按星期策略走
        result["priority"] = "weekday"
        result["recommended_type"] = week_strategy["best_types"][0]
        result["recommended_topic"] = None  # 由daily.py的内容包填充
        result["recommended_time"] = week_strategy["best_time"]
        result["reason"] = week_strategy["reason"]

    result["week_strategy"] = week_strategy
    result["upcoming_events"] = upcoming

    # 6. 检查正在进行的官方活动
    active_activities = get_active_official_activities()
    result["official_activities"] = active_activities

    # 7. 生成季节性AI提示词建议
    result["season_prompt_tips"] = (
        f"当前季节「{season['name']}」的推荐色调：{season['colors']}。"
        f"推荐画面主题：{season['subjects']}。"
        f"可参考画家：{season['painters']}。"
        f"AI关键词：{season['ai_keywords']}"
    )

    return result
