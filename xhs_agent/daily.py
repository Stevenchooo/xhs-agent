"""小红书运营Agent - 每日执行任务包（v2：基于真实数据优化）
数据发现：互动率好(点赞25%/收藏7%/CTR6.3%)但量不够→加密度+加新类型
新增：视觉反转型（#油画标签下最容易爆的类型）
文案风格：去AI味，参差不齐，有废话有情绪
"""

import datetime
import difflib
import re


def _attach_data_driven_context(package: dict) -> dict:
    """附加基于 tracker 的执行摘要字段；无数据时仍有兜底文案。"""
    try:
        from .strategy import get_data_driven_execution_brief
        from .tracker import get_adaptive_tool_profile

        brief = get_data_driven_execution_brief()
        adaptive = get_adaptive_tool_profile()
        package["data_driven_note"] = brief.get("note", "")
        package["tool_focus"] = brief.get("tool_focus") or []
        package["execution_focus"] = brief.get("execution_focus") or []
        package["weekly_update_note"] = adaptive.get("weekly_update_note", "")
        package["weekly_actions"] = adaptive.get("weekly_actions") or []
        package["adaptive_profile"] = adaptive
    except Exception:
        package.setdefault("data_driven_note", "数据暂不可用，请先完成笔记追踪后再试。")
        package.setdefault("tool_focus", [])
        package.setdefault("execution_focus", [])
        package.setdefault("weekly_update_note", "")
        package.setdefault("weekly_actions", [])
        package.setdefault("adaptive_profile", {})
    return package


def _normalize_text(value: str) -> str:
    """标准化标题/主题，便于和历史已发内容做弱匹配。"""
    return re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "", (value or "").lower())


def _get_package_topic_id(package: dict) -> str:
    """获取内容包稳定 topic_id；老包没有显式 ID 时退回到 theme/title 派生。"""
    explicit = package.get("topic_id")
    if explicit:
        return explicit
    fallback = package.get("theme") or package.get("title") or package.get("cover_text") or ""
    return _normalize_text(fallback)


def _package_text_candidates(package: dict) -> list:
    candidates = [
        _normalize_text(package.get("title", "")),
        _normalize_text(package.get("theme", "")),
        _normalize_text(package.get("cover_text", "")),
        _normalize_text(_get_package_topic_id(package)),
    ]
    for alias in package.get("dedupe_aliases", []) or []:
        candidates.append(_normalize_text(alias))
    return candidates


def _load_published_signals() -> dict:
    """读取已发布内容的 topic_id 与文本信号，供今日/本周排期避让。"""
    try:
        from .tracker import get_all_posts

        texts = []
        topic_ids = set()
        for post in get_all_posts():
            topic_id = _normalize_text(post.get("topic_id", ""))
            if topic_id:
                topic_ids.add(topic_id)
            for field in ("title", "notes"):
                normalized = _normalize_text(post.get(field, ""))
                if normalized:
                    texts.append(normalized)
        return {"topic_ids": topic_ids, "texts": texts}
    except Exception:
        return {"topic_ids": set(), "texts": []}


def _package_has_been_published(package: dict, published_signals: dict) -> bool:
    """判断内容包是否已发布过。优先 topic_id，再用 alias/title/theme 做弱匹配。"""
    candidates = [text for text in _package_text_candidates(package) if text]
    published_texts = published_signals.get("texts", []) or []
    published_topic_ids = published_signals.get("topic_ids", set()) or set()
    if _normalize_text(_get_package_topic_id(package)) in published_topic_ids:
        return True
    if not candidates or (not published_texts and not published_topic_ids):
        return False

    for candidate in candidates:
        for published in published_texts:
            if candidate == published:
                return True
            if candidate and published and (candidate in published or published in candidate):
                return True
            if len(candidate) >= 8 and len(published) >= 8:
                ratio = difflib.SequenceMatcher(None, candidate, published).ratio()
                if ratio >= 0.62:
                    return True
    return False


def _get_package_candidate_indices(target_date: datetime.datetime) -> list:
    """返回某一天的候选内容包索引，前面的优先级更高。"""
    weekday = target_date.weekday()
    candidates = []

    date_override_map = {
        (2026, 3, 17): 14,
        (2026, 3, 23): 14,
    }
    override_idx = date_override_map.get((target_date.year, target_date.month, target_date.day))
    if override_idx is not None:
        candidates.append(override_idx)

    if weekday == 4:
        candidates.append(14)

    weekday_map = {
        0: 12,
        1: 6,
        2: 8,
        3: 14,
        5: 5,
        6: 7,
    }
    default_idx = weekday_map.get(weekday, 14)
    candidates.append(default_idx)

    for idx in range(len(DAILY_PACKAGES)):
        if idx not in candidates:
            candidates.append(idx)
    return candidates


def _get_creative_candidate_indices(target_date: datetime.datetime) -> list:
    """按星期返回高想象力主题池的候选顺序。"""
    weekday = target_date.weekday()
    date_override_map = {
        (2026, 3, 30): [7, 0, 4],
    }
    override = date_override_map.get((target_date.year, target_date.month, target_date.day))
    if override is not None:
        preferred = list(override)
    else:
        weekday_map = {
            0: [0, 4, 1],
            1: [1, 0, 5],
            2: [2, 6, 3],
            3: [3, 1, 4],
            4: [5, 2, 6],
            5: [4, 6, 0],
            6: [6, 3, 2],
        }
        preferred = list(weekday_map.get(weekday, [0, 1, 2]))
    for idx in range(len(CREATIVE_PACKAGES)):
        if idx not in preferred:
            preferred.append(idx)
    return preferred


def _iter_candidate_packages(target_date: datetime.datetime):
    """先产出创意池，再回退到已验证基础池。"""
    seen_topic_ids = set()

    for idx in _get_creative_candidate_indices(target_date):
        package = CREATIVE_PACKAGES[idx].copy()
        topic_id = _get_package_topic_id(package)
        if topic_id not in seen_topic_ids:
            seen_topic_ids.add(topic_id)
            yield package

    for idx in _get_package_candidate_indices(target_date):
        package = DAILY_PACKAGES[idx].copy()
        topic_id = _get_package_topic_id(package)
        if topic_id not in seen_topic_ids:
            seen_topic_ids.add(topic_id)
            yield package


def _pick_unpublished_package(target_date: datetime.datetime) -> dict:
    """按优先级挑选一个未发布过的内容包；如果都发过则退回首个候选。"""
    published_signals = _load_published_signals()
    candidate_packages = list(_iter_candidate_packages(target_date))
    fallback = candidate_packages[0].copy()

    for package in candidate_packages:
        if not _package_has_been_published(package, published_signals):
            return package
    return fallback


# ==================== 内容包库（基于数据优化后） ====================
DAILY_PACKAGES = [

    # ===== Day 1：视觉反转型（新增·对标#油画Top1） =====
    {
        "day_label": "Day 1",
        "type": "视觉反转型",
        "theme": "放大AI油画10倍",
        "why": "#油画标签下Top1（10.4万赞）就是「放大10倍」的反转类型。你的AI油画天然适合做这个——厚涂肌理放大后视觉冲击力极强",
        "time": "21:00",
        "prompts": [
            {
                "desc": "图1·封面：一幅完整的AI油画（远景）",
                "prompt": "A stunning oil painting of a Venetian canal at sunset, thick impasto brushstrokes, rich warm amber and burnt sienna palette, canvas texture visible, gallery quality fine art, dramatic golden hour lighting --ar 3:4 --s 800 --v 6.1",
                "note": "这张是「远看」的全图",
            },
            {
                "desc": "图2-5：放大细节（极致特写）",
                "prompt": "Extreme macro close-up of thick oil paint impasto texture on canvas, individual brushstrokes clearly visible with paint ridges and valleys, warm amber and burnt sienna colors, museum quality painting surface detail, side lighting emphasizing texture depth --ar 1:1 --s 800 --v 6.1",
                "note": "多跑几张选最有质感的 放大到能看到「颜料的山丘」",
            },
            {
                "desc": "图6-7：另一幅画的远景+特写",
                "prompt": "Oil painting of spring cherry blossoms in a garden, soft pink and green palette, visible thick paint strokes, impressionist style, morning light, canvas texture --ar 3:4 --s 750 --v 6.1",
                "note": "换个色调再做一组远景→特写的对比",
            },
            {
                "desc": "图8-9：第三组对比或汇总图",
                "prompt": "（用Canva做对比图：左边全图→右边放大10倍的细节，加箭头标注）",
                "note": "最后1-2张做成明显的对比图 一眼就能看出差别",
            },
        ],
        "cover_text": "放大AI油画10倍后 我整个人不好了",
        "title": "放大AI油画10倍后 我整个人不好了",
        "body": """我一直觉得AI画的东西放大了肯定穿帮

直到我把这几幅放大了10倍看

……嗯？？？

这个颜料堆积的质感
这个笔触的纹理
这个画布的编织纹

等等 这真的是AI画的吗

我自己都开始怀疑了哈哈哈哈

向右滑看对比👉
左边是原图 右边是放大10倍后的细节

说实话第3张那个特写
我截出来发给学画画的朋友看
她说"这肌理感比我画的还真实"

好吧 被AI教做人了

📌 关键是
这些全是Midjourney生成的
参数我放评论区了 想试的自己拿

不过有个前提——
prompt里一定要加impasto和visible brushstrokes
不加的话放大了就是糊的
加了放大才有这种「颜料山丘」的效果

好了不说了
你们自己放大看吧
第几张最像真画？评论区说👇""",
        "hashtags": "#油画 #AI绘画 #AI油画 #Midjourney #油画肌理 #放大看细节 #当代艺术 #提示词分享 #艺术 #值得收藏",
    },

    # ===== Day 2：画家介绍·Richter =====
    {
        "day_label": "Day 2",
        "type": "画家介绍 + AI复刻",
        "theme": "Richter：把照片画模糊的男人",
        "why": "画家名字自带搜索流量，「故意画模糊→卖3亿」的反差是天然钩子。AI模仿他的模糊效果视觉冲击大",
        "time": "21:00",
        "prompts": [
            {
                "desc": "图1·封面：模仿Richter模糊风格",
                "prompt": "Oil painting of a rainy city street in Gerhard Richter photo-painting style, deliberately blurred and smeared with a squeegee, soft out-of-focus effect, muted grey and blue tones, wet reflections on asphalt, large canvas texture, contemporary art museum quality --ar 3:4 --s 800 --v 6.1",
                "note": "封面加文字「把照片画模糊→卖3亿」",
            },
            {
                "desc": "图2-3：Richter原作（WikiArt找高清图）",
                "prompt": "（不用生成 去WikiArt搜Gerhard Richter下载Betty/Lesende等代表作）",
                "note": "",
            },
            {
                "desc": "图4-5：AI模仿Richter不同题材",
                "prompt": "Portrait painting in Gerhard Richter blurred photo-realism style, a woman reading by the window, soft focus effect as if smeared with a palette knife, grey and muted flesh tones, photographic composition painted in oil, melancholic atmosphere --ar 3:4 --s 750 --v 6.1",
                "note": "",
            },
            {
                "desc": "图6-8：原作和AI版交替排列",
                "prompt": "Abstract painting in Gerhard Richter squeegee technique style, layers of paint dragged horizontally, vibrant red yellow blue beneath grey smears, thick impasto texture, large scale contemporary abstract --ar 3:4 --s 800 --v 6.1",
                "note": "原作/AI交替排 让人猜哪个是AI",
            },
        ],
        "cover_text": "他故意把画画模糊 然后卖了3个亿",
        "title": "他故意把画画模糊 然后卖了3个亿",
        "body": """你能想象吗

一个画家花好几周画了一幅超级写实的油画
然后——

拿一块刮板 一刮
全糊了

就这样 一幅画拍出了3亿人民币

我第一次知道的时候也觉得离谱
什么操作？？画完了再毁掉？？

他叫Gerhard Richter 里希特
德国人 今年94了
被叫做「在世最伟大的画家」

🎨 所以到底为什么「模糊」值3亿

Richter说过一句话我一直记着：
「照片是最完美的图像 而绘画是最完美的模糊」

他的意思是——
你以为你看到的是真实的？不是
记忆是模糊的
感知是模糊的
没有什么是100%清晰的

这哥们画的不是画
画的是一种哲学

我服了 真的

🤖 然后我让AI学他

用MJ跑了他的squeegee技法
出来的效果 远看还挺像那么回事

但近看就知道
AI能模仿那个模糊的视觉效果
但模仿不了一个94岁的老头
站在画布前犹豫要不要刮掉的那种心情

这大概就是人和AI的区别吧

Prompt放评论区了 想试的自取
你觉得AI能学会Richter吗？👇""",
        "hashtags": "#当代艺术 #油画 #GerhardRichter #里希特 #AI绘画 #画家故事 #艺术科普 #AI油画 #画家推荐 #西方油画",
    },

    # ===== Day 3：现实像油画型（新增·对标#油画Top4） =====
    {
        "day_label": "Day 3",
        "type": "现实像油画",
        "theme": "随手拍的照片vs AI画成油画",
        "why": "#油画Top4「我好像拍到了莫奈眼中的油画视界」3.9万赞。把现实照片→AI油画化是天然的对比向爆款内容",
        "time": "12:00",
        "prompts": [
            {
                "desc": "拍一张现实中像油画的照片（雨后路面/日落/水面倒影/雾中建筑）",
                "prompt": "（不用AI生成——用手机拍：雨后积水倒影 / 黄昏天空 / 树影斑驳的墙 / 雾蒙蒙的街道）",
                "note": "真实照片是这篇的核心素材！在上海随手拍就有很多油画感的场景",
            },
            {
                "desc": "用MJ把同一场景画成油画风格",
                "prompt": "Oil painting of [描述你的照片场景], impressionist style, visible brushstrokes, warm golden light, thick impasto texture, Monet-inspired plein air painting, canvas texture --ar 3:4 --s 750 --v 6.1",
                "note": "把[描述你的照片场景]替换成你实际拍的内容",
            },
        ],
        "cover_text": "在上海随手拍的 朋友问我这是莫奈的画吗",
        "title": "在上海随手拍的 朋友问我这是哪幅油画",
        "body": """上周下雨嘛
我在路上随手拍了张积水倒影的照片

发朋友圈之后有人问我：
"这是哪个美术馆的画？"

???
朋友 这是马路

然后我突发奇想
把这张照片丢给AI
让它"画"成真正的油画

结果出来之后
说实话 照片比AI画的还像油画
哈哈哈哈哈哈

向右滑看对比👉
第1张：我拍的原图
第2张：AI画的油画版

你觉得哪个更有油画感？

其实上海真的是一个很适合拍「油画感」照片的城市
雨天的倒影
黄昏的外滩
法租界的梧桐树影

随便拍拍都是莫奈色

📌 想拍出油画感的小tips
· 找水面倒影（雨后地面最好用）
· 黄昏的光线自带滤镜
· 逆光拍树叶 光斑碎成一片
· 雾天和阴天的颜色最莫兰迪

下次下雨别光躲雨了 拿起手机拍一张试试
说不定你身边就有一幅莫奈✨

你在哪个城市拍到过「油画感」的照片？发出来看看👇""",
        "hashtags": "#油画 #莫奈 #油画感 #上海 #AI绘画 #AI油画 #手机摄影 #城市摄影 #当代艺术 #治愈系",
    },

    # ===== Day 4：AI油画×生活跨界（新增·对标#油画Top6/7跨品类） =====
    {
        "day_label": "Day 4",
        "type": "AI油画×生活",
        "theme": "用AI给家里画了幅挂画",
        "why": "#油画Top6/7都是跨品类内容（油画妆/油画开箱），跨品类=双倍流量池。AI油画×家居是最好做的跨界方向",
        "time": "21:00",
        "prompts": [
            {
                "desc": "图1·成品效果图（画挂在墙上的照片）",
                "prompt": "（先用MJ生成一幅适合挂墙上的AI油画 然后用Canva/PS把画P到家里墙上 或者打印出来真的挂上去拍照）",
                "note": "如果能真的打印挂墙上拍照效果最好 照片打印店30-50块就能做",
            },
            {
                "desc": "图2：AI生成的原画",
                "prompt": "Large abstract oil painting for modern living room, soft sage green and cream white palette, minimal geometric forms, thick impasto texture, calming zen atmosphere, contemporary fine art, gallery quality --ar 3:4 --s 800 --v 6.1",
                "note": "选适合家居风格的——莫兰迪色/极简抽象最百搭",
            },
            {
                "desc": "图3-4：其他风格的AI挂画",
                "prompt": "Oil painting of ocean waves crashing on rocks, deep navy blue and seafoam white, dramatic brushstrokes, large format painting for living room, coastal interior design aesthetic --ar 3:4 --s 750 --v 6.1",
                "note": "",
            },
        ],
        "cover_text": "用AI给客厅画了幅挂画 朋友以为我花了大几千",
        "title": "用AI给客厅画了幅挂画 来的人都问在哪买的",
        "body": """事情是这样的

我一直想给客厅挂幅油画
但是去画廊看了一圈
便宜的看不上 好看的买不起

然后我想到了——

我自己用AI画一幅不就行了？

说干就干
打开Midjourney 调了半小时参数
出来一幅莫兰迪色的抽象画

然后去照片打印店
打印了一张60×80的
连框带打印一共花了45块

挂上去之后

朋友来我家第一句话：
"这画在哪买的？看着挺贵的"

我：45块 AI画的
朋友：……

哈哈哈哈哈不好意思让你失望了

📌 想自己做的话
关键是选对风格——
挂客厅选莫兰迪色/极简抽象
挂卧室选暖色调风景
挂书房选冷调几何

prompt里加上：for modern living room
AI就会自动往家居方向靠

尺寸建议60×80或50×70
淘宝搜"照片打印装裱" 几十块搞定

我把几个不同风格的prompt放评论区了
喜欢哪个自己拿去试

你家墙上挂的是什么？""",
        "hashtags": "#油画 #AI绘画 #家居装饰 #客厅装饰画 #AI油画 #挂画 #Midjourney #家居好物 #装修 #省钱装修",
    },

    # ===== Day 5：90后画家合集 =====
    {
        "day_label": "Day 5",
        "type": "艺术清单合集",
        "theme": "5位90后当代画家",
        "why": "合集类高收藏+「90后身价千万」反差强+年轻画家中文资料极少=信息差",
        "time": "18:30",
        "prompts": [
            {
                "desc": "封面：5位画家代表作拼图",
                "prompt": "（Canva做：5位画家代表作各截一块拼在一起 + 大标题）",
                "note": "从下面5位画家的作品各截一张拼封面",
            },
        ],
        "cover_text": "这5个90后画画的 身价已经过千万了",
        "title": "这5个90后画画的 身价已经过千万了…",
        "body": """我说真的
之前一直以为画家都是那种白胡子老爷爷
直到我查到这几个人的年龄

啊？？90后？？身价千万？？？

行吧 同样是90后 我在这刷手机
人家已经被佳士得拍卖了（哭

━━━━━━━━━━━━

1️⃣ Flora Yukhnovich 🇬🇧 1990年生

怎么形容她的画呢
就像有人把洛可可风格的蛋糕扔进了搅拌机
出来的全是粉色的奶油色的一坨坨
但就是好看 离谱的好看
2022年一幅画拍了2000万+ 她才32

2️⃣ Avery Singer 🇺🇸 1987年生

这个更野
她先用3D建模软件画草稿 然后再画到画布上
就 你能想象吗 画油画之前先开电脑建模
科技与狠活.jpg
作品均价500万+

3️⃣ Issy Wood 🇬🇧 1993年生

93年的！！
她画的东西特别诡异——皮手套、旧沙发、过时的首饰
看着不舒服但就是挪不开眼
被叫做「Z世代最重要的画家」
这title也太大了吧

4️⃣ Jadé Fadojutimi 🇬🇧 1993年生

也是93年的
画巨大的抽象画 颜色像炸了一样
泰特美术馆收藏过的最年轻艺术家之一
我连泰特的门都还没进过呢哈哈哈

5️⃣ Lucy Bull 🇺🇸 1990年生

用喷枪+油画的混合技法
画面看着像显微镜下的细胞组织
迷幻到不行 适合盯着看发呆

━━━━━━━━━━━━

我为什么要写这些人
因为现在知道=早
等她们以后封神了
你可以假装淡定地说"哦我很早就关注她了"

（装x利器 不谢

先🌟收着吧 以后聊天用得上
最喜欢谁？我后面单独写她👇""",
        "hashtags": "#当代艺术 #画家推荐 #90后画家 #油画 #艺术科普 #西方油画 #艺术合集 #画家 #值得收藏 #艺术",
    },

    # ===== Day 6：光影解析 =====
    {
        "day_label": "Day 6",
        "type": "色彩/构图解析",
        "theme": "油画里的光怎么画的",
        "why": "干货型内容收藏率高(15-25%)。周六发深度内容用户更有耐心看",
        "time": "10:00",
        "prompts": [
            {"desc": "伦勃朗光", "prompt": "Oil painting portrait with dramatic Rembrandt lighting, strong chiaroscuro, single light source from upper left, deep shadows on one side of the face, warm golden light against dark background, classical oil painting technique, thick impasto highlights --ar 3:4 --s 750 --v 6.1", "note": ""},
            {"desc": "印象派散射光", "prompt": "Impressionist oil painting of a garden scene in bright diffused sunlight, Claude Monet style dappled light through leaves, broken color technique, visible brushstrokes of complementary colors, vibrant outdoor luminosity --ar 3:4 --s 700 --v 6.1", "note": ""},
            {"desc": "维米尔窗户光", "prompt": "Interior painting with soft window light in Johannes Vermeer style, gentle light falling on a woman reading a letter, subtle gradation of light to shadow, luminous pearl-like skin tones, quiet domestic scene, Dutch Golden Age lighting --ar 3:4 --s 750 --v 6.1", "note": ""},
            {"desc": "透纳戏剧光", "prompt": "Dramatic seascape painting in JMW Turner style, explosive golden sunset light breaking through storm clouds, atmospheric light dissolving forms, romantic sublime landscape, thick swirling paint texture, raw natural power --ar 3:4 --s 800 --v 6.1", "note": ""},
        ],
        "cover_text": "同样画个苹果 伦勃朗和莫奈画出来完全不一样",
        "title": "同样画个苹果 伦勃朗和莫奈画出来完全不一样",
        "body": """想了很久要不要写这篇
因为感觉一讲到"光"就很容易变成美术课

但我尽量说人话 哈哈

简单来说就是
同样一个苹果放桌上
伦勃朗画出来像悬疑片
莫奈画出来像下午茶
维米尔画出来像时间停了

区别在哪？就在光

━━━━━━━━━━━━

🕯️ 伦勃朗光

就一个字：暗

画面一半亮一半暗 明暗对比拉到极致
人脸像被一盏聚光灯打了
其他地方全是黑的
效果：戏剧感直接拉满

你写AI prompt的时候加这个👇
dramatic Rembrandt lighting, strong chiaroscuro
直接出片

☀️ 印象派那种光

莫奈那帮人不在屋里画画 专门跑到外面去
然后就疯狂画阳光打在树叶上碎成一块一块的效果
颜色不混合 直接一笔红一笔绿戳上去
远看就是阳光洒下来的感觉

prompt加：
Impressionist dappled light, broken color
出来那个空气感 真的绝

🪟 维米尔的窗户光

这个我最喜欢

就是一扇窗户 光从左边照进来
照在一个在看信/倒牛奶/弹琴的人身上
特别安静 看着就想深呼吸

prompt：soft window light, Vermeer style
出来的图氛围感拿捏得死死的

🌅 透纳那种光

透纳的画吧 说实话 第一次看我没看懂
就感觉光和颜色炸了一整个画面
山也看不清 海也看不清
全被光吞掉了

但后来在美术馆看到原作我才理解
那种震撼是小图体会不到的

prompt：Turner dramatic light, atmospheric dissolving forms

━━━━━━━━━━━━

所以下次你画AI油画不知道选什么氛围的时候
直接对照这个选：

想安静 → 维米尔
想大片 → 伦勃朗
想清新 → 印象派
想炸裂 → 透纳

好了 先🌟存着 回头写prompt的时候翻出来抄

你平时最常用哪种光？""",
        "hashtags": "#油画 #色彩美学 #AI绘画 #艺术科普 #油画技法 #光影 #AI油画 #Midjourney #绘画教程 #值得收藏",
    },

    # ===== Day 7：Flora Yukhnovich 深度 =====
    {
        "day_label": "Day 7",
        "type": "画家故事",
        "theme": "Flora Yukhnovich·90后卖2000万",
        "why": "承接90后画家合集做深度介绍 中文零资料=信息差 90后身份自带话题",
        "time": "20:30",
        "prompts": [
            {"desc": "AI模仿Yukhnovich风格", "prompt": "Abstract painting in Flora Yukhnovich style, contemporary rococo reinterpretation, swirling pastel pink cream and lavender forms, Boucher-inspired sensuous curves dissolved into abstraction, candy-like luminous palette, oil paint with soft fluid brushwork --ar 3:4 --s 800 --v 6.1", "note": "封面加文字「90后 一幅画2000万」"},
            {"desc": "原作（画廊官网找图）", "prompt": "（搜Flora Yukhnovich Victoria Miro gallery 下载代表作）", "note": ""},
            {"desc": "AI模仿变体", "prompt": "Contemporary rococo oil painting, Flora Yukhnovich inspired, abstract garden party scene dissolving into pastel swirls, cream rose and mint green palette, Fragonard echoes in contemporary abstraction, dreamy sensual atmosphere --ar 3:4 --s 800 --v 6.1", "note": ""},
        ],
        "cover_text": "90后的她 一幅画卖了2000万",
        "title": "90后的她一幅画2000万 但大部分人没听过她名字",
        "body": """Flora Yukhnovich
弗洛拉·尤赫诺维奇
1990年 英国

一个你现在必须记住的名字

为什么？
因为她2022年的一幅画
在佳士得拍出了2000万+
那年她才32

🎨 她画的到底是什么

一句话：用当代的方式重新画洛可可

洛可可就是18世纪法国那种
粉粉的 华丽的 肉肉的宫廷画
代表是布歇和弗拉戈纳尔

Yukhnovich做了一件很聪明的事——
她把洛可可的粉色、曲线、肉感
全部打碎 搅成了抽象画

远看是一团粉色的梦
近看你能隐约发现身体的曲线和花瓣

既古典又当代
既甜美又有劲

说实话第一次看到她的画
我脑子里就一个字：好吃
像一整面墙的奶油蛋糕🍰

🤖 我用AI模仿了一下

关键词：Flora Yukhnovich style + contemporary rococo + pastel abstraction
效果居然意外地好 那种奶油流动感AI很擅长

但原作有一个AI做不到的东西——
你仔细看能发现抽象里藏着具象
那种若隐若现的感觉
AI还差点意思

📌 为什么要关注她

三个理由够了：
90后 女性 天价

中文互联网上关于她的介绍几乎是零
你现在看到的可能是最早的一批

收着吧🌟
5年后她火遍全球的时候
你可以说我早就知道了

觉得她的画好看吗？评论区说说👇""",
        "hashtags": "#当代艺术 #FloraYukhnovich #90后画家 #油画 #洛可可 #画家推荐 #AI油画 #画家故事 #西方油画 #艺术科普",
    },

    # ===== Day 8：莫兰迪合集 =====
    {
        "day_label": "Day 8",
        "type": "AI油画合集",
        "theme": "莫兰迪色系AI油画",
        "why": "合集类收藏率最高(18-30%) 莫兰迪色在小红书自带流量",
        "time": "21:00",
        "prompts": [
            {"desc": "莫兰迪色瓶罐静物", "prompt": "A still life painting of ceramic vases and bottles in muted Morandi color palette, soft grey-green and dusty pink tones, thick oil paint texture with visible brushstrokes, warm diffused lighting, minimal composition on a pale linen tablecloth, fine art museum quality --ar 3:4 --s 750 --v 6.1", "note": ""},
            {"desc": "莫兰迪色花卉", "prompt": "Oil painting of dried flowers in a grey ceramic vase, Morandi muted earth tones, dusty rose and sage green, soft shadows, impasto texture, contemplative still life atmosphere, painterly brushwork --ar 3:4 --s 700 --v 6.1", "note": ""},
            {"desc": "莫兰迪色窗边", "prompt": "A window scene painting in Giorgio Morandi color palette, sheer curtain with soft light, muted taupe and pale blue tones, a single pear on the windowsill, oil on canvas texture, serene and meditative mood --ar 3:4 --s 750 --v 6.1", "note": ""},
            {"desc": "莫兰迪色抽象", "prompt": "Abstract oil painting in Morandi muted palette, overlapping geometric shapes in dusty pink grey and sage, soft edges, visible canvas texture, contemplative minimalist composition, museum quality fine art --ar 3:4 --s 800 --v 6.1", "note": ""},
        ],
        "cover_text": "用AI画了一组莫兰迪色油画 每张都想当壁纸",
        "title": "用AI画了一组莫兰迪色油画 每一张都想存进手机",
        "body": """最近沉迷用AI画油画
这次挑战了我最爱的莫兰迪色系

就是那种灰灰的 柔柔的 高级感拉满的色调

说实话生成的时候我自己都惊了
AI居然能把厚涂质感做到这个程度
每一张放大看都有笔触纹理

🎨 关于莫兰迪色

Giorgio Morandi 意大利画家
一辈子只画瓶瓶罐罐
但他对色彩的理解影响了整个设计界

那种「高级灰」就是从他这来的
对 就是你在各种家装和穿搭里看到的那种灰粉灰绿

📌 AI出莫兰迪感的3个关键词

1️⃣ muted（低饱和度）
2️⃣ dusty（灰蒙蒙的质感）
3️⃣ soft shadows（柔和的阴影）

少了任何一个 颜色就会太跳 不够「莫兰迪」

参数：--s 700-800 --v 6.1

这组图随便拿去当壁纸吧
反正我手机已经换上了

你最喜欢哪一张？👇""",
        "hashtags": "#油画 #AI绘画 #莫兰迪色 #AI油画 #当代艺术 #Midjourney #色彩美学 #提示词分享 #手机壁纸 #值得收藏",
    },

    # ===== Day 9：AI vs Hockney =====
    {
        "day_label": "Day 9",
        "type": "AI vs 真实油画对比",
        "theme": "AI模仿Hockney泳池画",
        "why": "对比向话题性最强 Hockney泳池辨识度高 颜色鲜艳适合做封面",
        "time": "21:00",
        "prompts": [
            {"desc": "AI模仿Hockney泳池", "prompt": "Swimming pool painting in David Hockney style, bright turquoise water with geometric ripple patterns, California sunshine, modernist architecture in background, flat bold colors, acrylic on canvas texture, pop art influenced contemporary painting --ar 3:4 --s 750 --v 6.1", "note": ""},
            {"desc": "Hockney原作（网上找A Bigger Splash高清图）", "prompt": "（不用生成 下载原作）", "note": ""},
            {"desc": "AI版另一角度", "prompt": "Painting of a luxury swimming pool seen from above in David Hockney style, vivid cyan water, geometric diving board shadow, palm trees, bright flat colors with minimal shading, Southern California aesthetic --ar 3:4 --s 700 --v 6.1", "note": ""},
            {"desc": "AI版Hockney风景", "prompt": "Yorkshire landscape painting in David Hockney style, bright vivid greens and purples, rolling hills with geometric tree forms, bold outlined shapes, joyful spring colors, iPad painting aesthetic transferred to oil on canvas --ar 3:4 --s 750 --v 6.1", "note": ""},
        ],
        "cover_text": "让AI画Hockney的泳池 你猜哪张是真的",
        "title": "让AI画Hockney的泳池 你能分清哪张是真的吗",
        "body": """David Hockney
80多岁还在用iPad画画的英国老爷子
他的泳池画可能是当代艺术里最好认的

那种加州阳光下蓝到发光的水
几乎成了当代艺术的icon

所以我想试试——AI能画出Hockney的感觉吗？

🎨 先说结论：形可以 神差点

AI学到的：
✅ 标志性的青蓝色泳池水
✅ 几何化的水波纹
✅ 明亮饱和的加州色彩

AI没学到的：
❌ 他画水的那种「定格一瞬间」的感觉
❌ 80年积累的构图直觉
❌ 对加州生活的迷恋和乡愁

关于Hockney你可能不知道的事：
· 在世最贵艺术家之一 一幅画6.26亿
· 80多岁开始用iPad画画 说"iPhone是最小的画布"
· 从英国搬到加州 就因为被阳光和泳池迷住了

向右滑看对比👉
你猜哪张AI哪张原作？评论区说👇""",
        "hashtags": "#当代艺术 #DavidHockney #霍克尼 #AI绘画 #油画 #AI油画 #画家推荐 #泳池 #艺术科普 #当代艺术家",
    },

    # ===== Day 10：AI教程（你的数据验证的最强类型） =====
    {
        "day_label": "Day 10",
        "type": "AI绘画教程",
        "theme": "一个参数让AI油画从「假」变「真」",
        "why": "你的第一篇教程CTR6.3%+点赞率25%，数据验证这是你的强项，继续做",
        "time": "12:00",
        "prompts": [
            {"desc": "对比图：--s 200(低风格化)", "prompt": "Oil painting of a countryside cottage in autumn, warm colors --ar 3:4 --s 200 --v 6.1", "note": "低--s值 出来偏照片/插画感"},
            {"desc": "对比图：--s 500(中等)", "prompt": "Oil painting of a countryside cottage in autumn, warm colors --ar 3:4 --s 500 --v 6.1", "note": ""},
            {"desc": "对比图：--s 800(高风格化)", "prompt": "Oil painting of a countryside cottage in autumn, warm colors --ar 3:4 --s 800 --v 6.1", "note": "高--s值 出来绘画感最强"},
            {"desc": "对比图：--s 1000(极致)", "prompt": "Oil painting of a countryside cottage in autumn, warm colors --ar 3:4 --s 1000 --v 6.1", "note": "极致风格化 可能会过度 也展示一下"},
        ],
        "cover_text": "就改了一个数字 AI油画从「假」变「真」了",
        "title": "就改了一个数字 AI油画从假变真了",
        "body": """被问了无数次的一个问题：

"为什么我的AI油画看着像插画 你的看着像真画？"

答案可能比你想的简单
就一个参数：--s

--s是Midjourney的「风格化」参数
数字越高 画面越有「绘画感」
数字越低 越像照片或插画

我做了个对比实验👇
同一个prompt 只改--s的值

--s 200：像电脑壁纸 很清晰但一看就不是画
--s 500：开始有点画的意思了 但还差点
--s 800：对了！笔触出来了 颜料感出来了
--s 1000：有点过了 太抽象了 适合特定风格

所以日常画油画我的建议是：

--s 700-850 是甜区

低于600 → 数码感
高于900 → 太抽象

就这么简单
调一个数字 效果天差地别

不信你试试
把你之前觉得"不像油画"的prompt
后面加上 --s 800
看看变化大不大

试过之后来评论区告诉我效果怎样👇
效果好记得回来点赞哈哈哈""",
        "hashtags": "#AI绘画教程 #Midjourney教程 #AI油画 #油画 #提示词分享 #Midjourney #AI绘画 #AI艺术 #保姆级教程 #值得收藏",
    },

    # ===== Day 11：🔥 小红书官方活动·交换春天（03-10至04-30） =====
    {
        "day_label": "🌸 官方活动·交换春天",
        "type": "官方活动·春天AI油画",
        "theme": "用AI油画交换我的春天",
        "why": "小红书官方活动「我想和你交换春天」(03-10至04-30)，参与送流量加持！活动话题#交换春天，活动期间带话题发布可获得官方流量扶持，是冷启动期蹭流量的绝佳机会",
        "time": "12:00",
        "is_official_activity": True,
        "activity_info": {
            "name": "我想和你交换春天",
            "hashtag": "#交换春天",
            "period": "03-10 至 04-30",
            "benefit": "发春天赢流量",
        },
        "prompts": [
            {
                "desc": "图1·封面：春天花园的AI油画（高饱和度+特写+留白）",
                "prompt": "A stunning and vibrant Impressionist oil painting of a spring garden at golden hour, extreme macro close-up of thick impasto paint texture creating blooming cherry blossoms and fresh green leaves, rich saturated pink and emerald green palette, visible expressive brushstrokes, dappled sunlight, fine art museum quality, vertical 3:4 composition, bottom area slightly darker for text space --ar 3:4 --s 800 --v 6.1",
                "note": "选色彩最鲜艳的一张做封面，底部加白字「用AI画了9个春天的瞬间🌸｜哪个是你的春天」",
            },
            {
                "desc": "图2：春天的城市街道（樱花/玉兰）",
                "prompt": "Oil painting of a city street lined with blooming cherry blossom trees, petals falling like snow, wet pavement reflecting pink canopy, a bicycle leaning against a tree, impressionist style with visible brushstrokes, spring morning light, soft pastel pink and fresh green palette --ar 3:4 --s 750 --v 6.1",
                "note": "城市春天场景 贴近大家的日常",
            },
            {
                "desc": "图3：春天的菜场/市集（春菜春笋）",
                "prompt": "Still life oil painting of fresh spring vegetables at a market, bamboo shoots, green peas, spring onions, tender greens, arranged on rustic wooden table, warm natural light, thick impasto texture, vibrant fresh green and earth tones, canvas grain visible, cozy farmers market atmosphere --ar 3:4 --s 750 --v 6.1",
                "note": "春菜也是春天！贴合活动描述里的「在菜场遇到第一捧春菜」",
            },
            {
                "desc": "图4-5：春天的公园（拥抱大树/野餐/放风筝）",
                "prompt": "Impressionist oil painting of people in a spring park, a woman hugging a large old tree with fresh green leaves, scattered wildflowers on the grass, children flying kites in the background, warm dappled sunlight, Renoir-inspired joyful atmosphere, thick brushstrokes, pastel spring palette --ar 3:4 --s 800 --v 6.1",
                "note": "对应活动描述「在公园里拥抱一棵大树」",
            },
            {
                "desc": "图6：春天的夜游（夜樱/夜色公园）",
                "prompt": "Oil painting of a magical spring night walk, cherry blossoms illuminated by warm street lanterns, moonlight on a park path, fireflies dancing among flowers, dreamy atmosphere, dark blue and soft pink contrast, thick impasto texture, romantic impressionist night scene --ar 3:4 --s 800 --v 6.1",
                "note": "对应活动描述「一次夜游」春天的夜晚也很美",
            },
            {
                "desc": "图7：春天的写生/colorwalk",
                "prompt": "Oil painting of an artist painting en plein air in a spring meadow, easel and canvas facing a field of wildflowers, watercolor palette beside them, gentle breeze suggested by flowing grass, warm impressionist light, Monet outdoor painting atmosphere, thick brushstrokes --ar 3:4 --s 750 --v 6.1",
                "note": "对应活动描述「一次写生、一次colorwalk」",
            },
            {
                "desc": "图8：春天的一朵花特写（油画肌理放大）",
                "prompt": "Extreme close-up oil painting of a single spring flower blooming, thick impasto petals with paint ridges visible, morning dew drops on petals, fresh green stem, macro view of brushstroke texture, spring color palette of soft pink white and green, museum quality detail --ar 1:1 --s 800 --v 6.1",
                "note": "对应活动描述「拍下一朵花开的瞬间」 放大看油画肌理",
            },
            {
                "desc": "图9：汇总图/互动引导图",
                "prompt": "（Canva制作：左边放4张春天AI油画小图拼贴 + 右边文字「你的春天是什么？评论区交换🌸」+ 底部带#交换春天话题标签）",
                "note": "最后一张做互动引导 呼应官方活动主题",
            },
        ],
        "cover_text": "用AI画了9个春天的瞬间🌸｜哪个是你的春天",
        "title": "用AI画了9个春天的瞬间🌸｜哪个是你的春天",
        "body": """春天是什么？

小红书问我想不想交换春天
我想了想
我的春天大概是这样的——

是早上路过那棵玉兰树
突然发现它开了
是菜场里第一捧春笋的嫩绿色
是公园里那个抱着大树深呼吸的怪人（对 就是我
是下了班绕远路走一段樱花隧道
是某个晚上突然想出门走走
然后发现夜樱比白天更好看

这些都是春天吧

📌 于是我用AI把这些瞬间都画成了油画（AI辅助创作🤖）

印象派的光
厚涂的颜料
放大看每一笔都有春天的温度

向右滑看9个春天的瞬间👉

我最喜欢第3张——菜场春笋那幅
因为春天不只在花里
也在饭桌上啊 哈哈

🎨 关键prompt分享

想画出春天的感觉 核心关键词是：
· spring garden / cherry blossom（春天场景）
· impressionist（印象派=春天标配风格）
· fresh green and soft pink palette（春天配色）
· dappled sunlight（树影斑驳的光）
· thick impasto（厚涂=油画质感）

参数 --s 750-800 最合适
太低没有画感 太高太抽象

这组图存着当壁纸也很好看🌸

喜欢的朋友先🌟Mark住，文末有完整的AI绘画参数，春天出门找不到灵感可以翻出来照着画！

你的春天是什么？
在评论区跟我交换吧👇

⚠️ 本文图片由AI辅助生成
#交换春天""",
        "hashtags": "#交换春天 #油画 #AI绘画 #AI油画 #春天 #印象派 #Midjourney #提示词分享 #治愈系 #值得收藏",
    },

    # ==================== Day 8：蓝色主题AI油画（竞品验证的高赞色调） ====================
    {
        "day_label": "Day 8",
        "type": "AI油画合集",
        "theme": "一整组蓝色AI油画｜治愈系",
        "why": "竞品Osaki nana的Blue💙拿到8617赞，蓝色是油画赛道点赞率排名第一的色调，高饱和单色主题在信息流中极其抢眼",
        "time": "21:00",
        "prompts": [
            {
                "desc": "图1·封面：深蓝海面油画（最抢眼的做封面）",
                "prompt": "A stunning oil painting of deep ocean waves in rich cobalt blue and ultramarine, thick impasto paint strokes creating texture of moving water, dramatic underwater light filtering through surface, monochromatic blue palette with hints of turquoise and white foam, fine art museum quality, canvas texture visible --ar 3:4 --s 800 --v 6.1",
                "note": "选最震撼的一张做封面，加白色粗体标题",
            },
            {
                "desc": "图2：蓝色抽象油画（肌理特写）",
                "prompt": "Extreme close-up of abstract oil painting in monochromatic blue palette, thick layers of cerulean cobalt and prussian blue paint, swirling impasto ridges catching dramatic side light, deep ocean-like depth, tactile three-dimensional paint surface, contemporary fine art --ar 3:4 --s 800 --v 6.1",
                "note": "",
            },
            {
                "desc": "图3：蓝色花卉静物",
                "prompt": "Oil painting of blue hydrangeas in a dark ceramic vase, rich sapphire and periwinkle tones, thick painterly brushstrokes, moody blue-grey background, soft diffused window light, contemplative still life, visible canvas texture, Morandi-inspired composition --ar 3:4 --s 750 --v 6.1",
                "note": "",
            },
            {
                "desc": "图4：蓝色城市雨夜",
                "prompt": "Oil painting of a rainy city street at night in deep blue tones, wet reflections of neon lights on dark asphalt, cobalt blue sky with heavy clouds, impressionist style visible brushstrokes, atmospheric moody urban scene, thick impasto paint texture --ar 3:4 --s 750 --v 6.1",
                "note": "",
            },
            {
                "desc": "图5：蓝色山水风景",
                "prompt": "Landscape oil painting of misty blue mountains at dawn, layers of ultramarine and cerulean fading into pale blue sky, thick impasto paint creating mountain ridges, serene and meditative atmosphere, contemporary landscape art, visible brushwork --ar 3:4 --s 800 --v 6.1",
                "note": "",
            },
            {
                "desc": "图6：蓝色窗边场景",
                "prompt": "Interior oil painting of a window looking out to blue sea, sheer white curtain catching breeze, deep azure ocean visible through window, blue and white palette with warm wood tones, soft morning light, quiet domestic beauty, thick oil paint texture --ar 3:4 --s 750 --v 6.1",
                "note": "",
            },
            {
                "desc": "图7：蓝色冰川/北极光",
                "prompt": "Oil painting of northern lights aurora borealis over icy blue landscape, vivid electric blue and teal green sky, frozen lake reflecting colors, thick impasto paint creating light effects, magical arctic atmosphere, dramatic contemporary landscape --ar 3:4 --s 800 --v 6.1",
                "note": "",
            },
            {
                "desc": "图8-9：用以上Prompt微调，换场景（蓝色蝴蝶/蓝色鸢尾花/蓝色月光），保持蓝色主调统一",
                "prompt": "（复制以上任一Prompt，替换主体即可）",
                "note": "凑够9图，整组色调必须统一在蓝色系",
            },
        ],
        "cover_text": "一整组蓝💙｜看完整个人安静下来了",
        "title": "用AI画了一整组蓝💙｜看完整个人安静下来了",
        "body": """蓝色大概是油画里最治愈的颜色了

深海的蓝 雨夜的蓝 远山的蓝 窗外的蓝
每一种蓝都有不同的安静

这次用AI画了一整组蓝色油画
从海面到山脉 从花瓶到窗台
9张图 9种蓝 9种安静✨

🎨 关于蓝色在油画里的地位

你知道吗
在油画史上 蓝色曾经比黄金还贵
因为蓝色颜料要从阿富汗的青金石里提取
所以以前只有圣母玛利亚的长袍才配用蓝色

现在AI一个关键词就能出一整片蓝
但那种看着蓝色画面
心慢慢安静下来的感觉
几百年都没变过

📌 AI生成蓝色油画的关键词（AI辅助创作🤖）

想出好看的蓝 这几个词很重要：
· cobalt blue（钴蓝·最经典的油画蓝）
· ultramarine（群青·偏深偏紫的蓝）
· cerulean（天蓝·清透的蓝）
· monochromatic blue palette（单色蓝调色盘）
· thick impasto（厚涂质感）

参数建议 --s 800 出来的蓝色层次感更好

💡 个人觉得画蓝色主题有个小技巧：
不要纯蓝 要在蓝里混一点点灰或紫
这样蓝色才有「深度」而不是「塑料感」

🌟Mark住这组蓝色壁纸
下次心情烦躁的时候翻出来看看
比冥想管用 哈哈

你最喜欢哪种蓝？
第几张最让你安静？评论区告诉我👇

⚠️ 本文图片由AI辅助生成""",
        "hashtags": "#油画 #蓝色 #AI绘画 #AI油画 #治愈系 #Midjourney #色彩美学 #提示词分享 #值得收藏 #当代艺术",
    },

    # ==================== Day 9：高净值男性受众特化·天价艺术（Cy Twombly） ====================
    {
        "day_label": "Day 9",
        "type": "画家介绍 + AI复刻",
        "theme": "Cy Twombly：黑板上乱涂乱画卖4.5亿",
        "why": "基于3/10爆款数据（80%男性，65%>35岁），高净值熟龄人群极度喜欢「天价+反直觉」的商业/艺术逻辑探讨。这是完美的复刻版爆款公式",
        "time": "21:00",
        "prompts": [
            {
                "desc": "图1·封面：模仿Twombly的黑板涂鸦",
                "prompt": "Abstract painting in Cy Twombly blackboard style, continuous white looping scribbles on a dark grey chalkboard background, expressive and chaotic chalk-like lines, energetic gestures, large scale contemporary art masterpiece, dark and dramatic atmosphere, vertical 3:4, leaving empty space at the bottom for text --ar 3:4 --s 750 --v 6.1",
                "note": "封面用这张，加白字粗体：「黑板上乱画一通→拍出4.5亿」",
            },
            {
                "desc": "图2：Twombly原作《无题(纽约市)》（网上下载）",
                "prompt": "（不需要AI生成，去网上下载Cy Twombly《Untitled (New York City)》高清图）",
                "note": "展示这幅卖出7050万美元的原作",
            },
            {
                "desc": "图3：AI模仿其彩色时期作品",
                "prompt": "Abstract expressionist painting in Cy Twombly style, chaotic scribbles and energetic paint drips, vibrant red yellow and pink marks on a huge white canvas canvas, raw emotional energy, childish but sophisticated mark-making, museum quality contemporary art --ar 3:4 --s 800 --v 6.1",
                "note": "展示他不是只会画黑板",
            },
            {
                "desc": "图4：AI模仿其玫瑰系列",
                "prompt": "Abstract painting of blooming roses in Cy Twombly style, massive scale dripping red and pink paint, poetic and melancholic atmosphere, words scribbled faintly in the background, expressive gestural brushwork, contemporary fine art --ar 3:4 --s 750 --v 6.1",
                "note": "",
            },
        ],
        "cover_text": "在黑板上乱涂乱画居然拍出4.5亿💰｜是天才还是骗局",
        "title": "黑板上乱涂乱画居然卖了4.5亿💰｜凭什么这么贵",
        "body": """你能想象吗？
一块看起来就像小孩在黑板上乱涂乱画的画布
在苏富比拍卖行拍出了7050万美元（约4.5亿人民币）🤯

他就是「Cy Twombly」赛·托姆布雷
当代艺术史上最具争议，但也最受顶级藏家追捧的美国大师

🎨 他到底在画什么？

这幅卖出天价的《无题(纽约市)》
就是在一块深灰色的画布上
用白色的蜡笔画了整整6排连续的圈圈

很多人看的第一眼反应是：
“就这？我上幼儿园的儿子画得都比他好！”
“这绝对是洗钱骗局！”

但这恰恰是这幅画的牛逼之处👇

📌 为什么「乱涂乱画」反而这么值钱？

在这幅画诞生之前，艺术都在教人怎么画得“像”
但Twombly在做什么？
他为了忘掉自己极其扎实的学院派绘画技巧
关在黑屋子里，在黑暗中闭着眼睛画画

他不是在画一个“圈”
他是在画“画圈的这个动作”本身
他在记录一种纯粹的、连续的、没有任何目的性的能量流动

这不是技巧，这是解构规则的哲学 ✨
而在顶级资本圈，能够重新定义规则的东西，就是最贵的。

🤖 我让AI学他的黑板涂鸦（AI辅助创作🤖）

用Midjourney模仿了Twombly的黑板风格
关键Prompt：
「Cy Twombly blackboard style + continuous white looping scribbles + dark grey chalkboard background」

说实话，AI能精准模仿出那种圈圈的形状
但总觉得太“规矩”了——
少了他当年坐在朋友肩膀上，在巨大画布上滑动时那种失控的激情

你觉得这是天才的哲学，还是资本的炒作？
评论区聊聊👇

⚠️ 本文部分图片由AI辅助生成""",
        "hashtags": "#当代艺术 #CyTwombly #艺术收藏 #AI绘画 #画家推荐 #投资逻辑 #油画 #AI油画 #拍卖 #艺术史",
    },
    {
        "day_label": "Day 10",
        "type": "画家故事 + AI复刻",
        "theme": "David Hockney：80多岁还在iPad上画画",
        "why": "年龄反差+科技标签+高价成交，这类题既有搜索流量也有讨论性。相比纯泳池对比，更适合拉新关注和建立账号记忆点。",
        "time": "21:00",
        "prompts": [
            {
                "desc": "图1·封面：AI模仿Hockney泳池风格",
                "prompt": "Swimming pool painting in David Hockney style, bright turquoise water with geometric ripple patterns, California sunshine, crisp shadows, flat bold colors, modernist villa in the background, acrylic-to-oil texture, contemporary fine art poster composition, vertical 3:4 with space for headline at bottom --ar 3:4 --s 750 --v 6.1",
                "note": "封面加大字「80多岁 还在iPad上画画」",
            },
            {
                "desc": "图2：Hockney原作《A Bigger Splash》或泳池系列高清图",
                "prompt": "（不需要AI生成，去网上下载David Hockney《A Bigger Splash》或泳池系列原作高清图）",
                "note": "用原作建立辨识度和搜索感",
            },
            {
                "desc": "图3：AI模仿Hockney的iPad风景画",
                "prompt": "Landscape painting in David Hockney iPad drawing style, rolling Yorkshire hills in spring, bright vivid greens and purples, simplified tree forms, joyful thick digital brush lines translated into painterly texture, contemporary art, vertical 3:4 --ar 3:4 --s 750 --v 6.1",
                "note": "强调他晚年拥抱新工具这件事",
            },
            {
                "desc": "图4-5：AI模仿其窗景/室内花卉系列",
                "prompt": "Interior painting in David Hockney style, open window looking onto a sunlit garden, vase of flowers on a table, flat planes of vivid color, graphic outlines, bright optimistic atmosphere, painterly texture, contemporary British art --ar 3:4 --s 750 --v 6.1",
                "note": "和泳池系列交替排，画面会更丰富",
            },
        ],
        "cover_text": "80多岁 还在iPad上画画",
        "title": "80多岁还在iPad上画画 他凭什么卖到6亿？",
        "body": """很多人到80岁的时候
已经不太愿意学新东西了吧

但David Hockney不是

这位老爷子80多岁
还在iPad上画画
而且不是玩玩而已
是真的拿去做展览 卖高价 继续影响一代人

我第一次知道这事的时候
脑子里只有一个想法：

这也太酷了

🎨 他是谁

David Hockney
大卫·霍克尼
英国国宝级画家
在世最贵艺术家之一

很多人认识他
是因为那张特别有名的泳池画
蓝得像加州的夏天被定格住了

但我越来越觉得
他最厉害的不是画泳池
而是他从来不把工具当边界

年轻时画油画
后来玩摄影拼贴
再后来直接上iPad

别人一把年纪了开始怀旧
他一把年纪了还在更新系统

这真的很可怕

📌 他凭什么能一直值钱

不是因为会某一种技法
而是因为他总能把新的媒介
变成自己的语言

泳池也好 iPad也好
本质上他画的都是同一件事：
光
空间
还有那种让人想住进去的生活感

🤖 我顺手让AI学了下他的风格（AI辅助创作🤖）

颜色 学得很快
泳池的水波纹 也能学个七八分

但AI有个地方总差一点
它会画出漂亮的画面
却很难画出霍克尼那种
「我真的热爱生活」
的明亮劲儿

所以看到他80多岁还在iPad上画
我反而觉得
这不是科技新闻
这是一个艺术家最厉害的地方：
他一直没有停下来

你觉得画家的价值更重要的是技术
还是不断更新自己的眼光？👇

⚠️ 本文部分图片由AI辅助生成""",
        "hashtags": "#当代艺术 #DavidHockney #霍克尼 #iPad绘画 #画家故事 #AI绘画 #AI油画 #油画 #画家推荐 #艺术科普",
    },

    # ===== Day 11：名画破次元壁（今日主推） =====
    {
        "day_label": "Day 11",
        "type": "名画破次元壁",
        "theme": "赵本山×范伟：中式喜剧遇上西方名画",
        "why": "国民级喜剧人物 + 西方名画的强反差，自带点击和评论欲。今天主打『先笑一下，再被画面质感留住』的破圈内容。",
        "time": "21:00",
        "prompts": [
            {
                "desc": "图1·封面：赵本山×梵高（优先做成手持图）",
                "prompt": "Oil painting of a Chinese man looking like Zhao Benshan wearing Vincent van Gogh's green coat and fur hat with a bandaged ear, smoking a pipe, painted in van Gogh's post-impressionist style, thick impasto brushstrokes, vibrant orange and red background, museum quality --ar 3:4 --v 6.1 --s 500",
                "note": "生成后可合成到真实『手拿画纸』场景里，首图更像现实拍到的展览海报，点击率会更高。"
            },
            {
                "desc": "图2：范伟×蒙娜丽莎",
                "prompt": "Oil painting of a Chinese man looking like Fan Wei with a round face and glasses, wearing the costume of Mona Lisa, smiling mysteriously, painted in Leonardo da Vinci renaissance style, sfumato technique, classical landscape background, cracked oil paint texture --ar 3:4 --v 6.1 --s 500",
                "note": "这张负责做反差包袱：一本正经，但越看越绷不住。"
            },
            {
                "desc": "图3：赵本山与范伟×《呐喊》",
                "prompt": "Oil painting in Edvard Munch's The Scream style, two Chinese men looking like Zhao Benshan and Fan Wei standing on a bridge under a swirling red and orange sky, expressive wavy brushstrokes, existential angst mixed with comedic confusion --ar 3:4 --v 6.1 --s 600",
                "note": "荒诞感拉满，适合放在最后做压轴。"
            }
        ],
        "cover_text": "赵本山×范伟 乱入西方名画",
        "title": "名画破次元壁｜赵本山×范伟：中式喜剧遇上西方名画",
        "body": """如果赵本山和范伟突然闯进西方名画里
会发生什么？

我本来以为会很出戏
结果越看越不对劲

他们那种中式喜剧里的表情、停顿和关系感
放进古典油画的构图里
居然有一种奇怪的合理

一个负责让画面绷不住
一个负责让你越看越想笑

但最好玩的不是搞笑
而是这种反差真的会把画面记忆点拉满

向右滑看细节
第1张最适合做封面
第2张属于越看越离谱
第3张荒诞感直接拉满

下一期你最想看谁闯进名画里？
葛优、周星驰、沈腾，还是继续范德彪宇宙👇""",
        "hashtags": "#名画破次元壁 #赵本山 #范伟 #西方名画 #艺术脑洞 #搞笑油画 #当代艺术 #油画 #Midjourney #小红书创作灵感",
    },
]


CREATIVE_PACKAGES = [
    {
        "topic_id": "creative-vermeer-surveillance-night",
        "day_label": "Creative 1",
        "type": "反常理名画脑洞",
        "theme": "如果维米尔拍到了凌晨四点的监控画面",
        "why": "把古典静谧感和当代监控视角拼在一起，天然有反差，也更容易做出‘一眼停住’的新鲜感。",
        "time": "21:00",
        "dedupe_aliases": ["维米尔 监控画面", "凌晨四点 监控 名画"],
        "prompts": [
            {
                "desc": "图1·封面：维米尔式监控截图",
                "prompt": "Surveillance camera still in Johannes Vermeer style, a nearly empty convenience store aisle at 4 AM, cold fluorescent light transformed into soft pearl-like window light, quiet cinematic stillness, subtle Dutch interior realism, visible oil texture --ar 3:4 --s 700 --v 6.1",
                "note": "重点要做出“监控画面居然很高级”的违和感",
            },
            {
                "desc": "图2-4：不同凌晨场景",
                "prompt": "Oil painting of a 4 AM apartment corridor in Johannes Vermeer style, surveillance perspective from a high corner, one person holding milk and keys, soft silence, muted blue-grey palette, luminous skin tones, museum quality realism --ar 3:4 --s 700 --v 6.1",
                "note": "场景可以换成电梯口、走廊、楼下便利店",
            },
        ],
        "cover_text": "如果维米尔拍到了凌晨四点的监控画面",
        "title": "如果维米尔拍到了凌晨四点的监控画面",
        "body": """我最近突然在想一个问题

如果维米尔活在今天
他会不会根本不画窗边少女了

而是去截一张凌晨四点的监控画面

一个人拿着牛奶回家
便利店灯光冷得要命
电梯口空空的

这种画面按理说很“现实”
但一旦套进维米尔的光
居然有种安静到不敢说话的高级感

我试着用AI把这种时刻画成油画
出来的感觉很奇怪
不像复古
也不像未来
更像是“被生活偷偷拍下来的名画”

你们觉得第几张最像真的会挂进美术馆？
评论区告诉我👇""",
        "hashtags": "#维米尔 #油画 #当代艺术 #AI绘画 #AI油画 #名画脑洞 #美术馆 #深夜氛围 #艺术灵感 #值得收藏",
    },
    {
        "topic_id": "creative-convenience-store-between-hopper-hockney",
        "day_label": "Creative 2",
        "type": "风格对撞",
        "theme": "凌晨两点的便利店，夹在霍普和Hockney之间",
        "why": "Edward Hopper 的孤独和 Hockney 的明亮生活感是完全相反的两套气质，把它们放进同一场景，很容易形成讨论和记忆点。",
        "time": "21:00",
        "dedupe_aliases": ["霍普 Hockney 便利店", "凌晨两点 便利店 油画"],
        "prompts": [
            {
                "desc": "图1·封面：同一便利店场景做风格对撞",
                "prompt": "Late-night convenience store at 2 AM, split mood between Edward Hopper loneliness and David Hockney bright color geometry, fluorescent shelves, one customer choosing drinks, cinematic stillness, painterly oil texture --ar 3:4 --s 800 --v 6.1",
                "note": "封面文案要突出“同一场景 两种世界”",
            },
            {
                "desc": "图2-5：偏霍普/偏Hockney版本",
                "prompt": "Oil painting of a 2 AM convenience store in Edward Hopper style, lonely urban silence, long shadows, pale green fridge light, one figure standing still, melancholy cinematic realism --ar 3:4 --s 750 --v 6.1",
                "note": "再补一版 Hockney 风格做对照：bright turquoise, flat planes, California-like clarity",
            },
        ],
        "cover_text": "凌晨两点的便利店 夹在霍普和Hockney之间",
        "title": "凌晨两点的便利店，夹在霍普和Hockney之间",
        "body": """同样是一个便利店

Edward Hopper 来画
它会像一种城市病

David Hockney 来画
它又会像一部彩色电影的定格

我最喜欢这种完全不相干的两个人
被硬塞进同一个场景里

一个负责把夜色拉长
一个负责把颜色点亮

于是凌晨两点买水这种再普通不过的小事
突然就变成了可以挂墙上的东西

我让AI试着把这个场景分别往两边拉
结果比我想的还明显
同一盏灯
在不同画家手里真的是两个世界

如果只能选一边
你站霍普 还是站Hockney？👇""",
        "hashtags": "#EdwardHopper #DavidHockney #油画 #AI绘画 #风格对撞 #便利店美学 #当代艺术 #AI油画 #艺术脑洞 #小红书创作灵感",
    },
    {
        "topic_id": "creative-emotion-colorcards-resignation",
        "day_label": "Creative 3",
        "type": "情绪拟像合集",
        "theme": "把“想辞职但又不敢”画成9张油画色卡",
        "why": "情绪拟像天然适合评论互动，也能做收藏型内容；相比纯画家介绍，这类题更贴近日常情绪和分享欲。",
        "time": "21:00",
        "dedupe_aliases": ["情绪 色卡 油画", "想辞职但又不敢"],
        "prompts": [
            {
                "desc": "图1·封面：情绪色卡拼图",
                "prompt": "Nine-panel oil painting color study representing the feeling of wanting to quit your job but not daring to, muted office greys colliding with bruised blue and burnt orange, painterly texture, emotional abstract palette board --ar 3:4 --s 800 --v 6.1",
                "note": "适合做 9 宫格合集封面",
            },
            {
                "desc": "图2-9：具体情绪分镜",
                "prompt": "Abstract oil painting of emotional hesitation, office fluorescent light mixed with sunset orange hope, heavy blue-grey mood, thick brushstrokes, gallery-quality contemporary emotional painting --ar 3:4 --s 800 --v 6.1",
                "note": "可以拆成压抑、愤怒、麻木、想逃、想活一次等几个情绪",
            },
        ],
        "cover_text": "把“想辞职但又不敢”画成9张油画色卡",
        "title": "把“想辞职但又不敢”画成9张油画色卡",
        "body": """有些情绪其实很难说清

比如那种
每天都想辞职
但第二天还是准时打开电脑的感觉

它不是单纯的丧
也不是纯粹的愤怒
更像一堆很脏的颜色混在一起

所以我试了一件很无聊但又很好玩的事
把这种情绪拆成9种颜色
再让AI把它们画成油画

有一张像办公室空调吹到脸上的灰蓝
有一张像下班路上突然活过来的橘色
还有一张特别像你明明已经不爱了
但还是没辞职的那种土黄色

我知道这很抽象
但你们看到应该会懂

第几张最像你最近的状态？👇""",
        "hashtags": "#情绪色卡 #油画 #AI绘画 #AI油画 #当代艺术 #色彩美学 #打工人 #治愈系 #艺术灵感 #值得收藏",
    },
    {
        "topic_id": "creative-subway-pop-up-museum",
        "day_label": "Creative 4",
        "type": "城市瞬间再造",
        "theme": "如果上海地铁被临时改造成一间美术馆",
        "why": "把高频日常场景替换成美术馆语境，很容易形成代入感，也更像‘会被转发给朋友看’的城市脑洞题。",
        "time": "21:00",
        "dedupe_aliases": ["上海地铁 美术馆", "地铁站 临时 美术馆"],
        "prompts": [
            {
                "desc": "图1·封面：地铁站变美术馆",
                "prompt": "Shanghai metro station transformed into a temporary art museum, commuters walking past giant framed oil paintings, polished platform floor reflecting gallery lights, contemporary urban surrealism, painterly realism --ar 3:4 --s 800 --v 6.1",
                "note": "封面适合做“你每天路过的地方，其实像一间美术馆”",
            },
            {
                "desc": "图2-4：扶梯、站台、换乘通道",
                "prompt": "Oil painting of a subway escalator reimagined as an art gallery installation, commuters in neutral coats, dramatic museum spotlights, urban contemporary art atmosphere, rich painterly texture --ar 3:4 --s 750 --v 6.1",
                "note": "做成系列图，日常空间都能变得很像展览现场",
            },
        ],
        "cover_text": "如果上海地铁被临时改造成一间美术馆",
        "title": "如果上海地铁被临时改造成一间美术馆",
        "body": """我每天坐地铁的时候都会有一种错觉

有些站台其实特别像展览现场

只是我们走太快了
快到根本来不及把它当成一个画面去看

所以我试着做了一个很荒谬的想象
如果地铁站突然不再只是地铁站
而是一间临时美术馆

扶梯变成作品入口
站台灯光像展陈
换乘通道像大型装置

那些每天赶路的人
也一下子变得很像画里的人

最妙的是
你会发现城市里很多最普通的地方
其实只差一个观看方式

你最想把哪一个城市角落改造成美术馆？👇""",
        "hashtags": "#上海地铁 #美术馆 #油画 #AI绘画 #城市美学 #当代艺术 #AI油画 #艺术脑洞 #城市摄影 #值得收藏",
    },
    {
        "topic_id": "creative-richter-vlog-day",
        "day_label": "Creative 5",
        "type": "画家人格想象",
        "theme": "如果Richter也拍小红书，他的一天会有多无聊",
        "why": "把高冷大师人格化，会让内容更轻也更有分享感；同时仍然保留画家和风格本身的搜索价值。",
        "time": "21:00",
        "dedupe_aliases": ["Richter 小红书 一天", "里希特 vlog"],
        "prompts": [
            {
                "desc": "图1·封面：画家日常vlog感封面",
                "prompt": "Gerhard Richter imagined as a minimalist lifestyle vlogger, quiet studio morning, blurred photo-painting mood, coffee cup, paint scraper, soft grey light, painterly cinematic realism --ar 3:4 --s 750 --v 6.1",
                "note": "封面调性要像“无聊但高级”的日常记录",
            },
            {
                "desc": "图2-5：工作室、走路、看画、刮板细节",
                "prompt": "Oil painting of an elderly painter in a quiet contemporary studio, Gerhard Richter inspired mood, squeegee and blurred canvases, muted grey-blue palette, reflective and minimal atmosphere --ar 3:4 --s 750 --v 6.1",
                "note": "把大师拉回日常生活，会比纯介绍更有代入感",
            },
        ],
        "cover_text": "如果Richter也拍小红书 他的一天会有多无聊",
        "title": "如果Richter也拍小红书，他的一天会有多无聊",
        "body": """我最近老在想

如果里希特不是活在美术馆里
而是活在今天的小红书里

他会拍什么

不会是热闹的那种
大概率是：

早上喝一杯看起来很苦的咖啡
站在一幅快完成的画前发呆
拿刮板犹豫十分钟
最后还是把它刮糊

就这么结束一天

听起来很无聊
但又莫名很对

因为真正厉害的画家
可能本来就不是每天都在“灵感爆炸”
而是在重复、推翻、再重复

我把这种感觉试着画出来之后
突然觉得大师离我们也没那么远

如果是你
最想看哪位画家的“一天”？👇""",
        "hashtags": "#GerhardRichter #里希特 #油画 #AI绘画 #画家日常 #当代艺术 #AI油画 #艺术脑洞 #小红书vlog #艺术科普",
    },
    {
        "topic_id": "creative-deleted-ai-drafts-look-more-real",
        "day_label": "Creative 6",
        "type": "废稿反转",
        "theme": "那些差点被我删掉的AI油画废稿，为什么反而更像真画",
        "why": "废稿比成品更容易拉停留和讨论，因为用户天然想看‘翻车里藏着什么’。",
        "time": "21:00",
        "dedupe_aliases": ["AI油画 废稿", "差点删掉 更像真画"],
        "prompts": [
            {
                "desc": "图1·封面：故意保留瑕疵感的废稿",
                "prompt": "Oil painting draft with imperfect brushwork and unresolved composition, beautiful accident, painterly texture, visible correction marks, studio work-in-progress atmosphere, strangely more authentic than polished final art --ar 3:4 --s 800 --v 6.1",
                "note": "封面重点要让人看出‘没完成但更有味道’",
            },
            {
                "desc": "图2-4：不同类型的‘漂亮废稿’",
                "prompt": "Half-finished AI oil painting with raw brushstroke energy, color shifts, painterly mistakes becoming expressive, studio draft realism, contemporary art atmosphere --ar 3:4 --s 800 --v 6.1",
                "note": "可以做前后对照：废稿 vs 修完之后",
            },
        ],
        "cover_text": "那些差点被我删掉的AI油画废稿 反而更像真画",
        "title": "那些差点被我删掉的AI油画废稿，为什么反而更像真画",
        "body": """我以前做AI图有个毛病

一看到不够完整
第一反应就是删

但最近我翻以前的废稿
突然发现一个很奇怪的事

有些图虽然不完美
却比我最后修好的版本更像真画

可能是因为它们没那么“正确”
反而保留了那种画到一半的犹豫
和一点点失控

真正的油画本来就不是一上来就完美的
它会有改动
会有脏色
会有多出来的一笔

AI一旦太顺
反而容易失去那种人味

所以这次我把几张差点删掉的废稿翻出来
你们看看
是不是意外地比成品更有味道

第几张你会留下？👇""",
        "hashtags": "#AI油画 #油画 #AI绘画 #废稿 #创作过程 #当代艺术 #AI艺术 #艺术灵感 #提示词分享 #值得收藏",
    },
    {
        "topic_id": "creative-painters-groupchat-same-scene",
        "day_label": "Creative 7",
        "type": "群聊共创脑洞",
        "theme": "如果莫奈、Hockney、Richter在一个群里改同一张图",
        "why": "把大师风格差异做成人格化冲突，既能讲风格，也天然适合评论区站队。",
        "time": "21:00",
        "dedupe_aliases": ["莫奈 Hockney Richter 群聊", "同一张图 改图 大师"],
        "prompts": [
            {
                "desc": "图1·封面：三位画家改同一场景",
                "prompt": "Triptych oil painting showing the same city park scene interpreted by Claude Monet, David Hockney, and Gerhard Richter, each panel with distinct style, dramatic comparison, museum-quality composition --ar 3:4 --s 800 --v 6.1",
                "note": "封面适合做“三个人改同一张图，结果像三种人生”",
            },
            {
                "desc": "图2-4：单独展开每个人的版本",
                "prompt": "City park scene painted in Claude Monet style with dappled light and broken color, then in David Hockney flat bright geometry, then in Gerhard Richter blurred photo-painting mood, oil texture, contemporary comparison study --ar 3:4 --s 800 --v 6.1",
                "note": "一组内容就能把风格差异讲透",
            },
        ],
        "cover_text": "如果莫奈、Hockney、Richter在一个群里改同一张图",
        "title": "如果莫奈、Hockney、Richter在一个群里改同一张图",
        "body": """我有时候觉得
看不同画家改同一个场景
真的很像看一群性格完全不同的人在群里回消息

莫奈会先说
先别急 让我把光画碎一点

Hockney会说
颜色不够亮 再干净一点 再直接一点

Richter大概率一句话不说
直接给你糊掉

于是同一个场景
在三个人手里
就会变成三种完全不同的人生

这也是我现在最喜欢玩的一个方向
不是让AI只学一个人
而是让它把差异直接摊开给你看

如果只能选一个人替你改图
你会把这张图交给谁？👇""",
        "hashtags": "#莫奈 #DavidHockney #GerhardRichter #油画 #AI绘画 #风格对比 #当代艺术 #AI油画 #艺术科普 #评论区站队",
    },
    {
        "topic_id": "creative-jay-chou-klimt-easter-egg",
        "day_label": "Creative 8",
        "type": "流行文化×名画彩蛋",
        "theme": "周杰伦MV里最狠的，不是滤镜，是藏得最深的那幅名画",
        "why": "这轮数据已经验证“周董/大众IP + 名画彩蛋 + 强反差标题”是当前最能吃到首页推荐的一条线。今天继续沿着这条母题发，更适合承接爆量后的公域流量。",
        "time": "19:20",
        "dedupe_aliases": ["周杰伦 MV 名画彩蛋", "周董 克里姆特", "不是滤镜 是名画"],
        "prompts": [
            {
                "desc": "图1·封面：周董MV里的名画彩蛋主视觉",
                "prompt": "Realistic cinematic still from a luxurious Mandarin pop music video, East Asian male singer in black-and-gold ornate costume standing in a Klimt-inspired gilded hall, premium lensing, sharp skin texture, dramatic warm light, hidden Gustav Klimt visual language, believable MV screenshot --ar 3:4 --s 650 --v 6.1",
                "note": "如果直接发成品，优先用已生成的封面页；重跑时控制成更像真实MV截图而不是插画。",
            },
            {
                "desc": "图2·MV画面 vs 名画原型",
                "prompt": "Editorial comparison card, left side realistic Chinese music video frame in gold romantic atmosphere, right side Gustav Klimt reference painting, premium museum caption styling, ivory and muted gold accents, ultra clean and readable --ar 3:4 --s 500 --v 6.1",
                "note": "核心是把“原来高级感早就被名画写好了”这一层讲明白。",
            },
            {
                "desc": "图3·为什么会显得很贵",
                "prompt": "Realistic gold-toned corridor scene from a high-budget Mandarin music video, East Asian male pop star walking through Klimt-inspired architecture, dramatic backlight, authentic camera optics, detail analysis composition with room for annotations --ar 3:4 --s 650 --v 6.1",
                "note": "用来拆 3 个视觉线索：金色装饰密度、人物被图案包围、画面像名画构图。",
            },
            {
                "desc": "图4·评论区互动收束页",
                "prompt": "Luxury editorial end card for Xiaohongshu, warm ivory and muted gold, refined collector magazine style, elegant floral and ornamental borders, strong central typography area for interaction question, premium and minimal --ar 3:4 --s 450 --v 6.1",
                "note": "互动问题就问：你还想看哪支MV里的名画彩蛋？",
            },
        ],
        "cover_text": "周杰伦MV里最狠的 不是滤镜，是藏得最深的那幅名画",
        "title": "周杰伦MV里最狠的，不是滤镜，是藏得最深的那幅名画",
        "body": """以前看周杰伦MV
我只会觉得画面很贵

但这次重新看
我突然发现
最狠的不是滤镜
也不是布景

而是那些被偷偷塞进去的名画逻辑

尤其有几张画面
我第一眼就想到克里姆特

那种金色装饰感
人物像被花纹包围
画面很满
却一点都不乱

很多人会把这种感觉叫“高级”
但所谓高级感
很多时候并不神秘

它只是借用了名画早就验证过的东西
构图、色彩、装饰密度
还有那种一眼就让人停下来的视觉秩序

所以你以为自己在看周杰伦MV
其实也在看一场名画彩蛋局

我把最像的几张放在后面了
你们觉得第几张最明显？
如果你们愿意
我可以继续做这个系列：把MV、广告、电影海报里藏着的名画一个个扒出来。""",
        "hashtags": "#周杰伦 #周杰伦MV #名画彩蛋 #克里姆特 #油画 #艺术灵感 #审美提升 #小红书图文 #AI绘画 #当代视觉",
    },
]


def _get_weekday_package_index(target_date: datetime.datetime) -> int:
    """根据日期返回默认内容包索引。支持对特定日期做显式内容覆盖。"""
    return _get_package_candidate_indices(target_date)[0]


def get_today_package() -> dict:
    """获取今天的内容包（结合日历引擎智能推荐）
    优先级：官方活动（首次推荐）> 节日热点 > 星期策略
    """
    from .calendar_engine import get_smart_recommendation

    rec = get_smart_recommendation()

    # 0. 检查是否有正在进行的官方活动（官方活动优先级最高！参加送流量）
    official_activities = rec.get("official_activities", [])
    if official_activities:
        act = official_activities[0]  # 取第一个活动
        pkg_idx = act.get("daily_package_index")
        if pkg_idx is not None and pkg_idx < len(DAILY_PACKAGES):
            package = DAILY_PACKAGES[pkg_idx].copy()
            package["time"] = rec["recommended_time"]
            package["is_holiday"] = False
            package["is_official_activity"] = True
            package["official_activity"] = act
            package["date"] = rec["date"]
            package["weekday"] = rec["weekday"]
            package["smart_rec"] = rec
            return _attach_data_driven_context(package)

    # 1. 如果今天有节日热点，优先返回节日内容
    if rec["priority"] == "holiday" and rec.get("event"):
        event = rec["event"]
        package = {
            "day_label": f"🔥 {event['name']}特辑",
            "type": f"节日热点·{event['name']}",
            "theme": event["topic"].split("｜")[0] if "｜" in event["topic"] else event["topic"],
            "why": f"今天是{event['name']}（热度{event['heat']}），节日内容初始推荐量是平时的2-3倍，必须蹭！",
            "time": rec["recommended_time"],
            "prompts": [{"desc": "📌 用AI内容工坊生成节日主题Prompt", "prompt": f"请在Agent的「✍️ AI内容生成 → Step1·出Prompt」中，画面主题填写：{event['art_angle']}，风格参考选当季推荐", "note": "结合节日主题和当季色调"}],
            "cover_text": event["topic"],
            "title": event["topic"],
            "body": f"（请使用Agent的「✍️ AI内容生成 → Step2·反馈出文案」功能，描述你的AI生成结果，自动生成配套文案）\n\n节日角度：{event['art_angle']}",
            "hashtags": f"#{event['name']} #油画 #当代艺术 #AI绘画 #AI油画 #艺术 #值得收藏",
            "is_holiday": True,
            "event": event,
        }
    else:
        # 2. 按星期匹配最合适的内容包
        package = _pick_unpublished_package(datetime.datetime.now())
        package["time"] = rec["recommended_time"]
        package["is_holiday"] = False

    package["date"] = rec["date"]
    package["weekday"] = rec["weekday"]
    package["smart_rec"] = rec

    return _attach_data_driven_context(package)


def get_weekly_packages() -> list:
    """获取本周7天的内容包"""
    from .calendar_engine import CALENDAR_EVENTS, WEEKDAY_STRATEGY

    today = datetime.datetime.now()
    packages = []

    for i in range(7):
        date = today + datetime.timedelta(days=i)
        day_key = (date.month, date.day)
        weekday = date.weekday()
        day_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][weekday]
        strategy = WEEKDAY_STRATEGY[weekday]

        event = CALENDAR_EVENTS.get(day_key)
        if event:
            pkg = {
                "date": date.strftime("%m月%d日"),
                "weekday": day_name,
                "type": f"🔥 {event['name']}特辑",
                "theme": event["topic"].split("｜")[0] if "｜" in event["topic"] else event["topic"],
                "time": "12:00" if weekday < 5 else "10:00",
                "is_today": (i == 0),
                "is_holiday": True,
            }
        else:
            package = _pick_unpublished_package(date)
            pkg = {
                "date": date.strftime("%m月%d日"),
                "weekday": day_name,
                "type": package["type"],
                "theme": package["theme"],
                "time": strategy["best_time"],
                "is_today": (i == 0),
                "is_holiday": False,
            }
        packages.append(pkg)

    return packages
