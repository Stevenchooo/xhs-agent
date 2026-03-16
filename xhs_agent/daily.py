"""小红书运营Agent - 每日执行任务包（v2：基于真实数据优化）
数据发现：互动率好(点赞25%/收藏7%/CTR6.3%)但量不够→加密度+加新类型
新增：视觉反转型（#油画标签下最容易爆的类型）
文案风格：去AI味，参差不齐，有废话有情绪
"""

import datetime

# ==================== 10天内容包（基于数据优化后） ====================
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
]


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
            return package

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
        weekday = datetime.datetime.now().weekday()
        # 星期→内容包映射（基于第1周数据更新：互动率OK但曝光低，优先高冲击力内容）
        # 数据：封面CTR6.3%✅ 点赞率25%✅ 收藏率7.1%✅ 但曝光仅386→需要加量+加冲击力标题
        weekday_map = {
            0: 12, # 周一→Cy Twombly（复制爆款公式：反差+金钱+悬疑）
            1: 6,  # 周二→Flora（90后画家一幅画2000万，延续天价路线）
            2: 8,  # 周三→AI vs Hockney对比（话题性冲评论）
            3: 1,  # 周四→画家介绍Richter（信息差内容）
            4: 11, # 周五→蓝色AI油画合集🆕（竞品验证蓝色=点赞王，CTR冲8%）
            5: 5,  # 周六→光影解析（深度长文周末发）
            6: 7,  # 周日→莫兰迪AI油画合集（视觉治愈）
        }
        idx = weekday_map.get(weekday, 0)
        package = DAILY_PACKAGES[idx].copy()
        package["time"] = rec["recommended_time"]
        package["is_holiday"] = False

    package["date"] = rec["date"]
    package["weekday"] = rec["weekday"]
    package["smart_rec"] = rec

    return package


def get_weekly_packages() -> list:
    """获取本周7天的内容包"""
    from .calendar_engine import CALENDAR_EVENTS, WEEKDAY_STRATEGY

    today = datetime.datetime.now()
    packages = []

    weekday_map = {0: 12, 1: 6, 2: 8, 3: 1, 4: 11, 5: 5, 6: 7}

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
            idx = weekday_map.get(weekday, 0)
            pkg = {
                "date": date.strftime("%m月%d日"),
                "weekday": day_name,
                "type": DAILY_PACKAGES[idx]["type"],
                "theme": DAILY_PACKAGES[idx]["theme"],
                "time": strategy["best_time"],
                "is_today": (i == 0),
                "is_holiday": False,
            }
        packages.append(pkg)

    return packages
