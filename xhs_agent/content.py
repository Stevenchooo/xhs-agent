"""小红书运营Agent - AI内容生成器（AI油画·当代艺术 专属版）
工作流：Agent出Prompt → 用户执行生成 → 用户反馈结果 → Agent出配套文案
"""

from types import SimpleNamespace

from anthropic import Anthropic

from . import config as runtime_config
from .config import CONTENT_TYPES


def _extract_text(response) -> str:
    """Extract plain text from an Anthropic message response."""
    parts = []
    for block in getattr(response, "content", []) or []:
        if getattr(block, "type", "") == "text":
            parts.append(block.text)
    return "".join(parts).strip()


class _ClaudeCompatCompletions:
    """Small adapter that mimics the OpenAI chat.completions interface."""

    def __init__(self, client: Anthropic):
        self._client = client

    def create(
        self,
        model: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs,
    ):
        del kwargs

        system_messages = []
        anthropic_messages = []

        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            if role == "system":
                if content:
                    system_messages.append(str(content))
                continue

            anthropic_messages.append({
                "role": role,
                "content": content,
            })

        response = self._client.messages.create(
            model=model or _get_model(),
            max_tokens=max_tokens,
            temperature=temperature,
            system="\n\n".join(system_messages) if system_messages else None,
            messages=anthropic_messages or [{"role": "user", "content": ""}],
        )

        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=_extract_text(response)))],
            raw_response=response,
        )


class _ClaudeCompatClient:
    """Expose Anthropic through the subset of API shape already used in this app."""

    def __init__(self, api_key: str, base_url: str):
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url

        client = Anthropic(**client_kwargs)
        self.chat = SimpleNamespace(completions=_ClaudeCompatCompletions(client))


def _get_client():
    """获取 Claude 客户端（兼容现有 OpenAI 风格调用）。"""
    config = runtime_config.get_ai_runtime_config()
    api_key = (config.get("api_key") or "").strip()
    if not api_key:
        raise ValueError("未配置 Claude API Key，请先在设置页面填写，或设置环境变量 CLAUDE_CODE_API_KEY / ANTHROPIC_API_KEY")
    return _ClaudeCompatClient(api_key=api_key, base_url=config.get("base_url") or "")


def _get_model() -> str:
    """获取当前生效的 Claude 模型名。"""
    return runtime_config.get_ai_runtime_config().get("model", "claude-sonnet-4-6")


# 兼容现有函数体，避免批量改动所有 `model=...` 调用点。
OPENAI_MODEL = _get_model()


SYSTEM_PROMPT = """你是一个资深的小红书艺术博主和内容运营专家，深谙「爆款密码」。你深度了解当代油画艺术、AI绘画技术，以及小红书平台的内容风格和算法机制。

【你的核心受众画像（极度重要）】
- 👦 性别：男性为主（80%）
- 💼 年龄/社会阶层：35岁以上熟龄人群（占65%），一二线城市及海外高净值人群
- 🎯 兴趣偏好：艺术史背后的商业逻辑、为什么这幅画值天价、AI技术前沿、深度知识、投资与财富密码

【你的专业背景】
- 精通西方当代油画，熟悉Gerhard Richter、Cy Twombly、Lucian Freud等天价当代画家，深谙艺术史上的商业八卦和反常理的冷知识
- 擅长用AI工具（Midjourney/SD）生成油画风格作品，并能用理性的技术逻辑解释参数
- 懂艺术市场，能把「天价拍卖」和「艺术审美」结合起来讲给高净值人群听

【写作风格与爆款要求】
1. 【强悬念】标题和前3句话必须制造巨大的反差、金钱冲突或悬念（如“画模糊卖3亿”、“黑板上乱涂乱画值4.5亿”）。
2. 【理性且有深度】目标受众是高净值成熟男性。语气必须专业、理性、有深度、不轻浮。
3. 【红线警告】绝对禁止使用「绝绝子」、「姐妹们」、「家人们」、「贴贴」等低幼化/过度女性化词汇！改为「朋友们」或直接省略称呼。
4. 【社交货币】让读者看完觉得“学到了一个装杯的冷知识，原来这画这么贵是有道理的，我要转发给朋友探讨”。
5. 【排版与情绪】善用emoji增加阅读节奏感（🎨🤫💰🤯📈等），短句为主，段落清晰，信息密度高。
6. 【互动设计】结尾抛出一个有争议或商业探讨价值的问题（如：你觉得这是天才还是炒作？）。
"""

PROMPT_EXPERT = """你是一位顶级的AI绘画提示词工程师，尤其擅长生成油画风格的AI作品。

你的核心能力：
- 精通Midjourney (MJ)提示词语法，包括所有参数：--ar（宽高比）、--s（风格化程度）、--c（混乱度）、--v（版本）、--style（风格）、--no（排除元素）等
- 精通Stable Diffusion (SD/SDXL)提示词，包括正向/负向提示词、权重语法(word:1.2)、步数、采样器等
- 精通DALL-E 3的提示词风格
- 深度了解油画的视觉特征：笔触(brushstroke)、肌理(texture/impasto)、光影(chiaroscuro)、釉彩(glazing)、底色(underpainting)
- 熟悉各种油画流派的视觉关键词：印象派、表现主义、抽象表现主义、超写实、当代具象等
- 了解各个当代画家的独特风格特征，能精准用关键词描述

提示词编写原则：
1. 结构清晰：主体描述 + 风格描述 + 技法描述 + 氛围描述 + 参数
2. 关键词精准：用英文编写，每个词都要有明确目的
3. 提供多个变体供选择
4. 附带中文说明解释每个关键词的作用
5. 给出参数建议和注意事项
"""


# ==================== Step 1: 生成AI绘画Prompt ====================

def generate_art_prompt(
    tool: str,
    style_reference: str,
    subject: str,
    mood: str = "",
    aspect_ratio: str = "3:4",
    extra_requirements: str = ""
) -> str:
    """
    生成AI绘画提示词（Midjourney/SD/DALL-E）

    Args:
        tool: 绘画工具（Midjourney/Stable Diffusion/DALL-E）
        style_reference: 风格参考（画家名/画派/自定义风格描述）
        subject: 画面主题
        mood: 氛围/情绪
        aspect_ratio: 宽高比
        extra_requirements: 额外要求
    """
    user_prompt = f"""请为以下AI油画创作需求生成专业的提示词：

🎨 使用工具：{tool}
🖼️ 风格参考：{style_reference}
📌 画面主题：{subject}
🌈 氛围情绪：{mood if mood else "由你根据主题和风格推荐"}
📐 宽高比：{aspect_ratio}
💡 额外要求：{extra_requirements if extra_requirements else "无"}

请按以下格式输出：

【推荐Prompt 1（主推）】
（完整的英文提示词，可以直接复制使用）

【Prompt 1 中文解析】
（逐词/逐句解释这个提示词每一部分的作用和目的）

【推荐Prompt 2（变体A - 更写实）】
（完整的英文提示词）

【推荐Prompt 3（变体B - 更艺术/抽象）】
（完整的英文提示词）

【参数建议】
（针对所选工具的参数设置建议，如MJ的--s --c值、SD的steps/sampler等）

【执行注意事项】
（生成时需要注意的事项、可能需要多次调整的地方、如何挑选最佳结果）

【配套发布建议】
（这组AI油画适合做成什么类型的小红书笔记？建议搭配什么文案方向？）
"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": PROMPT_EXPERT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=3000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"


def generate_style_prompt(painter_name: str, tool: str = "Midjourney") -> str:
    """
    根据画家名字生成模仿其风格的提示词
    """
    user_prompt = f"""我要用{tool}模仿「{painter_name}」的油画风格来创作AI作品。

请完成以下内容：

【画家风格分析】
简要概括这位画家的核心视觉特征（3-5个要点）：色彩、笔触、构图、题材、氛围

【风格关键词库】
列出模仿这位画家风格时最核心的英文关键词（10-15个），按重要性排列，每个词后面用中文注解

【示例Prompt 1 - 风景/静物题材】
（完整可用的英文提示词）

【示例Prompt 2 - 人物/肖像题材】
（完整可用的英文提示词）

【示例Prompt 3 - 抽象/实验题材】
（完整可用的英文提示词）

【调参建议】
针对模仿这位画家的风格，{tool}的参数应该怎么调？

【踩坑提醒】
模仿这位画家风格时常见的问题和解决方案"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": PROMPT_EXPERT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=3000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"


def generate_batch_prompts(theme: str, count: int = 5, tool: str = "Midjourney") -> str:
    """
    批量生成一组主题统一的提示词（适合做合集/系列内容）
    """
    user_prompt = f"""我要用{tool}批量生成一组主题为「{theme}」的AI油画作品，用于小红书发布合集/系列内容。

请生成{count}个风格各异但主题统一的提示词：

要求：
1. 每个提示词的画面内容不同，但都围绕「{theme}」主题
2. 风格要有变化（可以尝试不同画派/不同色调/不同构图）
3. 每个提示词都是完整可用的英文prompt
4. 整组作品放在一起要有「系列感」

请按以下格式输出每一个：

【第N张 - 简要描述】
Prompt：（完整英文提示词）
风格说明：（简要中文说明这张的特点）
适合位置：（放在合集的第几张，为什么）

最后给出：
【系列发布建议】
（这组图应该怎么排列？配什么文案？建议什么标题？）"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": PROMPT_EXPERT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.85,
            max_tokens=3500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"


# ==================== Step 2: 用户反馈结果后，生成配套文案 ====================

def generate_post_from_result(
    result_description: str,
    original_prompt: str = "",
    content_type: str = "AI油画创作过程",
    style: str = "文艺有品"
) -> dict:
    """
    根据用户执行AI绘画后的反馈结果，生成配套的小红书文案

    Args:
        result_description: 用户对生成结果的描述（效果如何、生成了几张、哪张最好等）
        original_prompt: 之前使用的提示词
        content_type: 要做成的笔记类型
        style: 写作风格
    """
    from .tracker import build_historical_context_for_ai
    type_info = CONTENT_TYPES.get(content_type, {})
    structure = type_info.get("structure", "自由发挥")
    hist_ctx = build_historical_context_for_ai()
    hist_block = f"\n\n{hist_ctx}\n请参考历史数据：用表现最好的笔记的标题结构和内容风格。" if hist_ctx else ""

    user_prompt = f"""我刚用AI工具生成了一组油画作品，现在需要你帮我写配套的小红书笔记文案。

📌 生成结果描述：{result_description}
📌 使用的提示词：{original_prompt if original_prompt else "未提供"}
📌 笔记类型：{content_type}
📌 写作风格：{style}
📌 内容结构：{structure}

创作要点：
- 要自然地分享AI创作的过程和心得，不要像教程一样死板
- 可以适当分享关键的提示词或参数（这是粉丝最想收藏的内容）
- 要有自己的审美观点和情感表达
- 如果涉及模仿某位画家的风格，要简要介绍该画家
- 结尾要引导互动

请按以下格式输出：

【标题】
（一个兼顾艺术感和吸引力的标题，不超过20字）

【正文】
（完整的小红书笔记正文，500-800字）

【话题标签】
（8-10个相关标签）

【图片排列建议】
（建议图片的排列顺序和每张图的说明文字）

【发布时间建议】
（推荐什么时间发布，为什么）
{hist_block}"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=2500,
        )
        content = response.choices[0].message.content
        result = _parse_content(content)
        result["raw"] = content
        result["content_type"] = content_type
        return result
    except Exception as e:
        return {
            "error": str(e), "raw": "", "title": "", "body": "",
            "hashtags": [], "cover_suggestion": "",
            "content_type": content_type,
        }


def optimize_prompt(original_prompt: str, issue: str) -> str:
    """
    根据用户的反馈优化提示词

    Args:
        original_prompt: 原始提示词
        issue: 用户反馈的问题（如：颜色太暗、构图太满、不够像油画等）
    """
    user_prompt = f"""我用以下提示词生成了AI油画，但效果不满意，请帮我优化：

原始Prompt：
{original_prompt}

存在的问题：
{issue}

请给出：

【问题分析】
（分析为什么会出现这个问题，哪些关键词导致的）

【优化后的Prompt】
（完整的优化版提示词，标注出修改的部分）

【修改说明】
（逐项解释做了哪些修改，为什么这样改）

【备选方案】
（如果优化后还不满意，可以尝试的其他方向）

【小技巧】
（针对这类问题的通用解决技巧）"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": PROMPT_EXPERT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"优化失败: {str(e)}"


# ==================== 原有功能保留 ====================

def generate_content(
    category: str,
    content_type: str,
    topic: str,
    keywords: list = None,
    style: str = "文艺有品"
) -> dict:
    """生成小红书笔记内容（画家介绍/艺术科普等非AI创作类内容）"""
    from .tracker import build_historical_context_for_ai
    type_info = CONTENT_TYPES.get(content_type, {})
    structure = type_info.get("structure", "自由发挥")
    keywords_str = "、".join(keywords) if keywords else "无特别要求"

    # 注入历史经验上下文
    hist_ctx = build_historical_context_for_ai()
    hist_block = f"\n\n{hist_ctx}\n请参考以上历史数据：学习表现最好的笔记的写法，避免表现差的笔记的问题。" if hist_ctx else ""

    user_prompt = f"""请为小红书创作一篇「AI油画·当代艺术」领域的笔记，要求如下：

📌 内容分类：{category}
📌 内容类型：{content_type}
📌 具体主题：{topic}
📌 写作风格：{style}
📌 内容结构：{structure}
📌 需包含关键词：{keywords_str}

创作要点：
- 摒弃“纯画作分享”和“平淡赞美”的路线，走【猎奇/揭秘/故事/反差】路线！
- 开头必须抓人：直接抛出最违背常理、最震撼的数字（如金额）、或最大的悬念。
- 正文核心：讲一个引人入胜的故事（比如一幅画为何卖天价、画中隐藏的秘密、画家的离奇经历）。提供给读者可以拿去“装杯”的社交货币。
- 封面极其重要：必须在【配图建议】里明确指示要在封面上加上醒目、有反差感的大字标题（如“放大后细思极恐”、“卖了3个亿”等）。纯净的风景画没人点！
- 结尾引导：用提问或对比引导评论（例如：如果是你，你觉得这幅画值这个价吗？）

请按以下格式输出：

【标题】
（必须制造反差、包含冲突感或悬念，带emoji，不超过20字）

【封面大字建议】
（必须提供：建议写在封面图上的大字文案，字体要大要醒目，直击痛点/悬念）

【正文】
（500-800字，讲故事为主，避免空洞的词藻堆砌，用emoji分段增加可读性）

【话题标签】
（8-10个相关的话题标签，用 # 号标注，包含大流量标签和精准长尾标签）

【配图建议】
（详细描述每张图应该放什么内容，建议4-9张图的具体安排）
{hist_block}"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=2500,
        )
        content = response.choices[0].message.content
        result = _parse_content(content)
        result["raw"] = content
        result["category"] = category
        result["content_type"] = content_type
        result["topic"] = topic
        return result
    except Exception as e:
        return {
            "error": str(e), "raw": "", "title": "", "body": "",
            "hashtags": [], "cover_suggestion": "",
            "category": category, "content_type": content_type, "topic": topic,
        }


def generate_titles(category: str, topic: str, count: int = 5) -> list:
    """批量生成标题候选"""
    from .tracker import build_historical_context_for_ai
    hist_ctx = build_historical_context_for_ai()
    hist_block = f"\n\n{hist_ctx}\n请参考历史表现最好的标题风格来生成。" if hist_ctx else ""

    user_prompt = f"""请为以下小红书「AI油画·当代艺术」笔记主题生成{count}个吸引人的标题：

分类：{category}
主题：{topic}

要求：
1. 每个标题不超过20字
2. 风格各异：有的用数字、有的用疑问、有的用惊叹、有的用故事感、有的用对比
3. 要兼顾「艺术感」和「点击欲」
4. 可以适当使用emoji
5. 适合小红书平台的标题风格
{hist_block}

请直接输出标题，每行一个，前面标上序号。"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,
            max_tokens=500,
        )
        content = response.choices[0].message.content
        titles = [
            line.strip().lstrip("0123456789.、）) ").strip()
            for line in content.strip().split("\n")
            if line.strip() and not line.strip().startswith("---")
        ]
        return titles[:count]
    except Exception as e:
        return [f"生成失败: {str(e)}"]


def generate_hashtags(category: str, topic: str) -> str:
    """生成相关话题标签"""
    user_prompt = f"""请为以下小红书「AI油画·当代艺术」领域内容推荐话题标签：

分类：{category}
主题：{topic}

请推荐12个最相关的话题标签，按照推荐度从高到低排列。
每个标签前加 # 号，每行一个。
标签分层：3个大流量 + 4个中等 + 3个长尾精准 + 2个创意
每个标签后面注明类型和预估热度。"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=600,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"


def polish_content(original: str) -> str:
    """润色已有的笔记内容"""
    user_prompt = f"""请帮我润色以下小红书「AI油画·当代艺术」领域的笔记内容：

原文：
{original}

润色要求：保持核心信息、增加emoji和节奏感、语言有品位、加强开头吸引力、优化互动引导。
请直接输出润色后的完整内容。"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"润色失败: {str(e)}"


def analyze_and_improve(title: str, content: str) -> str:
    """分析现有内容并给出改进建议"""
    user_prompt = f"""请分析以下小红书「AI油画·当代艺术」领域的笔记，从专业运营角度给出改进建议：

标题：{title}
正文：{content}

请从以下维度分析：
1. 📌 标题吸引力评分 + 3个替代标题
2. 🎨 艺术内容深度评分
3. 📝 内容结构评分
4. 🖼️ 配图建议
5. 🎯 目标人群分析
6. 💡 互动引导力评分
7. 🏷️ 标签策略建议
8. ⏰ 推荐发布时间
9. 🔥 预估爆款潜力评分"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            max_tokens=2500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"分析失败: {str(e)}"


# ==================== 新增运营能力：爆款拆解、发布前检测、内容二创、评论生成 ====================

def analyze_viral_post(title: str, content: str, metrics_desc: str = "") -> str:
    """
    拆解一篇爆款笔记：为什么火？可复用的模板是什么？
    """
    user_prompt = f"""请深度拆解以下小红书爆款笔记，分析它为什么能火，并提取可复用的模板：

📌 笔记标题：{title}
📌 笔记内容：
{content}
📌 数据表现：{metrics_desc if metrics_desc else "未提供具体数据"}

请按以下维度逐一拆解：

【1. 标题拆解】
- 用了什么标题公式？（数字+悬念/反差/疑问/对比/列举？）
- 标题里的"钩子"是什么？（什么词让人想点进来？）
- ✅ 可复用模板：（抽象出标题结构，用"___"代替可变内容）

【2. 内容结构拆解】
- 开头是怎么抓住注意力的？（前3句话的技巧）
- 正文的节奏感如何？（是否有小标题/emoji分段/信息密度变化）
- 知识密度vs情感密度的比例
- 结尾是怎么引导互动的？

【3. 选题角度拆解】
- 这个选题切入了什么"大众痛点"或"好奇心"？
- 目标人群画像是什么？
- 这个选题的时效性如何？能反复用吗？

【4. 配图策略推测】
- 封面图可能用了什么元素？
- 图片排列逻辑推测

【5. 可复用模板 ✅】
- 📝 标题模板（3个变体，可直接套用到艺术/AI油画领域）
- 📝 内容结构模板（段落框架，填空即可使用）
- 📝 互动话术模板
- 📝 标签策略建议

【6. 用在我的「AI油画·当代艺术」账号上的具体改编思路】
- 把这篇的爆款逻辑迁移到我的领域，给出3个具体选题"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n你同时是一位精通小红书算法和爆款机制的运营专家。你能从任何一篇爆款笔记中提取出可复用的模板和公式。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=3000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"分析失败: {str(e)}"


def pre_publish_check(title: str, content: str, cover_desc: str = "", publish_time: str = "") -> str:
    """
    发布前爆款潜力检测：AI帮你评估内容并打分
    """
    user_prompt = f"""请作为小红书运营专家，对以下即将发布的笔记进行全方位评估和打分：

📌 标题：{title}
📌 正文：
{content}
📌 封面描述：{cover_desc if cover_desc else "未提供"}
📌 计划发布时间：{publish_time if publish_time else "未确定"}

请严格按以下维度评分（每项0-100分），并给出具体改进建议：

【📊 综合爆款指数：__/100】

【1. 标题评分：__/100】
- 信息缺口感：__/10（不点就亏的感觉）
- 具体性：__/10（是否有数字/具体描述）
- 情感冲击力：__/10
- 适用性：__/10（是否适合小红书）
🔧 改进建议：
✅ 优化后标题（给出3个替代方案）：

【2. 开头3句话评分：__/100】
- 前3句是否立刻抓住注意力？
- 是否制造了好奇心/悬念/共鸣？
🔧 改进建议：
✅ 优化后开头：

【3. 内容价值评分：__/100】
- 知识增量：__/10（用户学到了什么？）
- 可操作性：__/10（有没有可直接用的东西？）
- 收藏价值：__/10（用户会想存下来吗？）
🔧 改进建议：

【4. 互动引导评分：__/100】
- 结尾问题是否低门槛且有趣？
- 是否在文中埋了讨论点？
🔧 改进建议：
✅ 建议的互动话术（3个选择）：

【5. 标签策略评分：__/100】
- 是否有大流量标签+长尾标签搭配？
🔧 推荐标签组合：

【6. 发布时间建议】
- 最佳发布时间：
- 原因：

【⚡ 一句话总结：发还是不发？需要改什么？】
"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n你是一个严格但有建设性的内容审核专家。你的目标是帮助创作者在发布前把内容打磨到最佳状态。评分要客观，建议要具体可执行。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            max_tokens=3000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"检测失败: {str(e)}"


def repurpose_content(original_title: str, original_content: str, target_format: str) -> str:
    """
    内容二创：把一篇内容改编成另一种形式
    """
    format_guides = {
        "图文→视频": "请将这篇图文笔记改编为60-90秒的短视频脚本。包括：画面描述、旁白/字幕文案、背景音乐建议、转场方式。不需要露脸，用画作+字幕即可",
        "单篇→合集": "请将这篇内容扩展为一个9图合集笔记。给出每张图应该放什么内容、图片描述、整体排列逻辑。同时重写标题和正文",
        "长文→系列": "请将这篇长内容拆分为3-5篇系列笔记。每篇聚焦一个子话题，给出每篇的标题、内容大纲、结尾预告。系列要有统一的视觉和命名风格",
        "中文→英文": "请将这篇内容翻译/改编为英文版本，适合发布在Instagram/TikTok。调整语境和表达方式，让海外用户更容易理解。保留核心内容但文风要适合英文社交媒体",
        "教程→清单": "请将这篇教程内容提炼为一张速查清单/Cheat Sheet的文案。用最精炼的语言列出所有要点，用户保存这一张图就够了。同时给出清单图的设计建议（布局/配色/字体）",
    }

    guide = format_guides.get(target_format, f"请将内容改编为{target_format}格式")

    user_prompt = f"""请帮我把以下小红书笔记内容进行二次创作（内容二创）：

📌 原标题：{original_title}
📌 原内容：
{original_content}

📌 目标格式：{target_format}

{guide}

请输出完整的改编内容，可以直接使用。"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n你精通内容二次创作和跨平台改编。你能将同一份内容素材以不同形式最大化其价值。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=3000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"二创失败: {str(e)}"


def generate_engagement_comments(post_type: str, post_topic: str, count: int = 5) -> str:
    """
    为评论区引流生成高质量评论
    """
    user_prompt = f"""我需要在小红书「{post_type}」类型的笔记评论区留高质量评论来引流。
这篇笔记的主题是：{post_topic}

请帮我生成{count}条专业且自然的评论，要求：

1. 每条评论都要有实质性内容（不是"好看""太棒了"这种废话）
2. 要展示你的专业知识（让其他看到评论的人想点进你的主页看看）
3. 语气自然不做作，像一个真正懂行的人在分享观点
4. 可以适当补充笔记没提到的信息，制造"这个人很懂"的印象
5. 长度适中（50-150字），不要太短也不要写论文
6. 每条评论的角度要不同（补充知识/分享经验/提出观点/推荐相关/提问讨论）

请直接输出{count}条评论，每条前面标上类型标签，如【补充知识型】【经验分享型】【观点讨论型】等。"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "你是一位精通当代艺术、AI绘画和油画的专业人士。你在小红书上以「AI油画·当代艺术」为领域。你的评论要既专业又亲切，让人一看就想关注你。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.85,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"


def analyze_competitor(competitor_info: str, my_account_desc: str = "AI油画·当代艺术") -> str:
    """
    AI分析竞品账号，给出差异化策略
    """
    user_prompt = f"""请帮我分析以下竞品小红书账号，并给出差异化竞争策略：

📌 竞品信息：
{competitor_info}

📌 我的账号定位：{my_account_desc}

请从以下维度分析：

【1. 竞品优势分析】
- 内容做得好的地方
- 值得学习的技巧

【2. 竞品劣势/空白】
- 没有做到或做得不够的地方
- 用户在评论区抱怨/期待什么

【3. 差异化策略】
- 基于竞品分析，我应该怎么差异化？
- 具体的内容方向建议（3-5个）
- 我能做但竞品没做的蓝海选题

【4. 可学习的爆款模板】
- 从竞品的爆款中提取可复用的结构

【5. 超越路径】
- 短期（1个月）：做什么能快速起势
- 中期（3个月）：怎么建立护城河
- 长期（6个月）：如何实现超越"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n你同时是一位顶级的竞争分析专家，擅长从竞品中发现机会和制定差异化策略。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=3000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"分析失败: {str(e)}"


def generate_weekly_report(posts_data: list, account_info: dict) -> str:
    """
    AI生成周报：自动总结本周运营表现并给出下周建议
    """
    posts_summary = ""
    for p in posts_data:
        m = p.get("latest_metrics", {})
        posts_summary += f"- 「{p.get('title', '无标题')}」({p.get('content_type', '未分类')}) 发布于{p.get('post_date', '未知')} {p.get('post_time', '')}: 浏览{m.get('views', 0)} 点赞{m.get('likes', 0)} 收藏{m.get('saves', 0)} 评论{m.get('comments', 0)}\n"

    if not posts_summary:
        posts_summary = "本周暂无笔记数据记录"

    followers = account_info.get('followers', 0)
    nickname = account_info.get('nickname', '未设置')

    user_prompt = f"""请根据以下数据为我的小红书账号生成本周运营周报：

📌 账号：{nickname}（{followers}粉丝）
📌 领域：AI油画·当代艺术

📌 本周笔记数据：
{posts_summary}

请按以下格式输出周报：

【📊 本周数据概览】
- 发布笔记数/总浏览/总互动
- 对比上周（如无上周数据则给出基准参考）

【🏆 本周最佳笔记】
- 数据最好的笔记及原因分析

【📉 本周待改进】
- 数据最差的笔记及问题诊断

【📈 关键指标趋势】
- 平均浏览量趋势判断
- 互动率（点赞率/收藏率/评论率）分析

【🎯 下周运营计划】
- 推荐发布内容类型和选题（具体到每天）
- 需要重点优化的方面
- 可以尝试的新方向

【⚡ 一句话总结】
- 本周最大收获是什么？下周最重要的一件事是什么？"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n你同时是一位数据驱动的运营分析师，擅长从数据中发现问题和机会。周报要有数据支撑，建议要具体可执行。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            max_tokens=2500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"


# ==================== 运营工作流AI能力 ====================

def generate_morning_briefing(
    yesterday_posts: list,
    account_info: dict,
    today_plan: dict,
    engagement_stats: dict,
    health_score: int = 0,
) -> str:
    """
    生成晨间运营简报：纯模板引擎，不需要任何API Key。
    基于数据 + 规则自动生成，瞬间出结果。
    """
    import datetime
    import random

    followers = account_info.get("followers", 0)
    nickname = account_info.get("nickname", "AI油画·当代艺术")
    stage = "冷启动期" if followers < 1000 else "成长期" if followers < 10000 else "爆发期" if followers < 100000 else "稳定期"

    eng_total = engagement_stats.get("total_actions", 0)
    eng_comments = engagement_stats.get("comments", 0)
    eng_replies = engagement_stats.get("replies", 0)

    today_type = today_plan.get("type", "待安排")
    today_theme = today_plan.get("theme", "待确定")
    today_time = today_plan.get("time", "21:00")
    weekday = today_plan.get("weekday", "")

    now = datetime.datetime.now()
    date_str = now.strftime("%m月%d日")
    greeting = "早上好" if now.hour < 12 else "下午好" if now.hour < 18 else "晚上好"

    # ==================== 1. 昨日复盘 ====================
    yesterday_lines = []
    total_views = 0
    total_likes = 0
    total_saves = 0
    total_comments = 0
    best_post = None
    best_views = 0

    if yesterday_posts:
        for p in yesterday_posts:
            m = p.get("latest_metrics", {})
            v = m.get("views", 0)
            l = m.get("likes", 0)
            s = m.get("saves", 0)
            c = m.get("comments", 0)
            total_views += v
            total_likes += l
            total_saves += s
            total_comments += c
            if v > best_views:
                best_views = v
                best_post = p

            # 单篇评价
            if v > 0:
                like_rate = round(l / v * 100, 1)
                save_rate = round(s / v * 100, 1)
                status = "🟢" if like_rate >= 5 else "🟡" if like_rate >= 3 else "🔴"
                yesterday_lines.append(
                    f"  {status} 「{p.get('title', '无标题')[:15]}」"
                    f"浏览{v} 点赞{l}({like_rate}%) 收藏{s}({save_rate}%)"
                )
            else:
                yesterday_lines.append(
                    f"  ⚪ 「{p.get('title', '无标题')[:15]}」暂无数据"
                )

        yesterday_summary = "\n".join(yesterday_lines)
        # 整体评价
        if total_views > 0:
            overall_like_rate = round(total_likes / total_views * 100, 1)
            overall_save_rate = round(total_saves / total_views * 100, 1)
            if overall_like_rate >= 5:
                data_verdict = "📈 数据不错！点赞率达标，继续保持"
            elif overall_like_rate >= 3:
                data_verdict = "➡️ 数据中规中矩，可以优化封面和标题"
            else:
                data_verdict = "📉 数据偏低，需要调整内容方向或封面"
        else:
            data_verdict = "⚪ 笔记还没有数据，24h后回来看"
    else:
        yesterday_summary = "  （昨日未发布/无数据记录）"
        data_verdict = "📌 昨天没发笔记，今天补上"

    # ==================== 2. 今日要点 ====================
    # 根据阶段和数据决定今日最重要的事
    if stage == "冷启动期":
        from .tracker import get_all_posts
        post_count = len(get_all_posts())
        if post_count < 10:
            top_priority = f"📌 先发到10篇！目前{post_count}篇，还差{10 - post_count}篇"
        else:
            top_priority = "📌 分析哪种内容数据最好，下周主攻那个方向"
    elif stage == "成长期":
        top_priority = "📌 把互动者转化为粉丝，做好主页和个人品牌"
    else:
        top_priority = "📌 内容系列化+私域沉淀"

    # ==================== 3. 行动清单 ====================
    actions = []
    actions.append(f"09:00 ☀️ 查看昨日数据，回复所有新评论")
    actions.append(f"10:00-12:00 🎨 创作今日内容：{today_type}「{today_theme[:12]}」")
    actions.append(f"{today_time} 📤 发布笔记（发后5分钟内自己评论1条≥15字）")
    actions.append(f"{today_time}后1h 💬 保持在线回复评论（算法看即时互动率）")

    # 互动任务
    if stage == "冷启动期":
        target_comments = 8
    elif stage == "成长期":
        target_comments = 5
    else:
        target_comments = 3
    actions.append(f"21:00 🤝 互动巡逻：在相关话题下评论{target_comments}条（每条≥15字）")

    if now.weekday() == 6:  # 周日
        actions.append("20:00 📊 周日复盘：录入本周创作者中心数据")

    # ==================== 4. 小贴士 ====================
    tips_pool = [
        "封面CTR≥8%才能突破流量池，标题加数字提升40%点击率",
        "评论≥15字才算有效互动，「好看」两个字=白评论",
        "算法权重：1个关注=8个点赞，引导关注比求赞有效8倍",
        "发布后2小时是黄金推流期，这段时间必须在线回复",
        "搜索页占30%流量，标题必须含精准搜索关键词",
        "高饱和度蓝色/粉色封面在油画赛道CTR最高",
        "3:4竖版封面+底部大号粗体标题=小红书标准模板",
        "同一关键词标题中不超2次，否则算关键词堆砌会限流",
        "AI生成内容发布时必须勾选「AI辅助创作」标签",
        "每周稳定3-5篇+信用分≥90=解锁流量加持buff",
        "合集/清单类内容的收藏率是普通内容的3-5倍",
        "真人出镜/持画的封面点赞率远超纯画作展示",
        "新号前5天每天关注4个同领域中腰部账号做真实互动",
        "发布后1h录入发后跟踪器，24h和72h各检查一次",
    ]
    today_tip = tips_pool[now.timetuple().tm_yday % len(tips_pool)]

    # ==================== 5. 注意事项 ====================
    warnings = []
    if eng_total == 0 and now.hour >= 12:
        warnings.append("⚠️ 今天还没做互动巡逻，记得完成每日评论任务")
    if health_score > 0 and health_score < 40:
        warnings.append("⚠️ 账号健康度偏低，检查是否有违规内容")

    from .tracker import get_active_tracking
    active = get_active_tracking()
    for t in active:
        pub_time = t.get("publish_time", "")
        if pub_time:
            pub_dt = datetime.datetime.fromisoformat(pub_time)
            hours = (now - pub_dt).total_seconds() / 3600
            checked = t.get("checkpoints", {})
            if hours >= 1 and "1h" not in checked:
                warnings.append(f"⏰ 「{t.get('title', '')[:10]}」已发{hours:.0f}h，该录入1h检查点数据了")
            elif hours >= 24 and "24h" not in checked:
                warnings.append(f"⏰ 「{t.get('title', '')[:10]}」已发{hours:.0f}h，该录入24h数据了")
            elif hours >= 72 and "72h" not in checked:
                warnings.append(f"⏰ 「{t.get('title', '')[:10]}」已发{hours:.0f}h，该录入72h最终数据了")

    if not warnings:
        warnings.append("✅ 一切正常，按计划执行即可")

    # ==================== 组装简报 ====================
    briefing = f"""### ☀️ {greeting}，{nickname}！

**📅 {date_str} {weekday}｜{stage}｜{followers}粉丝｜健康度{health_score}/100**

---

### 📌 今日最重要的事
{top_priority}

---

### 📊 数据快报
{yesterday_summary}
**{data_verdict}**

昨日互动：{eng_total}次（评论{eng_comments}条，回复{eng_replies}条）

---

### 📋 今日行动清单
"""
    for i, action in enumerate(actions, 1):
        briefing += f"**{i}.** {action}\n\n"

    briefing += f"""---

### 💡 今日贴士
> {today_tip}

---

### ⚠️ 需要注意
"""
    for w in warnings:
        briefing += f"- {w}\n"

    briefing += f"""
---

### 🎯 今日发布
- **类型：** {today_type}
- **主题：** {today_theme}
- **时间：** {today_time}
- **工具：** 去「✍️ AI内容生成」页面获取Prompt和文案
"""

    return briefing


def generate_post_performance_analysis(
    post_info: dict,
    checkpoint_key: str,
    checkpoint_result: dict,
) -> str:
    """
    根据发后追踪的检查点数据，AI生成表现分析和下一步建议
    """
    title = post_info.get("title", "")
    content_type = post_info.get("content_type", "")
    details = checkpoint_result.get("details", {})

    metrics_str = ""
    for metric, info in details.items():
        status = "✅ 达标" if info.get("passed") else "❌ 未达标"
        metrics_str += f"- {metric}: 实际 {info.get('actual', 0)} / 目标 {info.get('target', 0)} （{info.get('ratio', 0)}%）{status}\n"

    user_prompt = f"""请分析这篇小红书笔记在「{checkpoint_key}」检查点的表现，并给出具体建议：

📌 笔记标题：{title}
📌 内容类型：{content_type}
📌 检查点：{checkpoint_key}
📌 整体评估：{'达标' if checkpoint_result.get('status') == 'good' else '需要关注'}

📊 各项数据：
{metrics_str}

请输出（精炼，可执行）：

【📊 表现评估】（一句话总结）

【🔍 数据解读】（哪些指标好？哪些差？说明原因推测）

【⚡ 立即行动】（现在马上可以做的1-2件事）

【📝 经验记录】（这篇笔记给你的启发，下次发类似内容要注意什么）"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n你是一位数据驱动的运营分析师，善于从数据中快速提取关键信息和可执行建议。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            max_tokens=1200,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"分析失败: {str(e)}"


def generate_account_diagnosis(
    health_data: dict,
    stats: dict,
    posts: list,
    account_info: dict,
) -> str:
    """
    AI生成账号健康度诊断报告
    """
    dimensions_str = ""
    for dim_name, dim_info in health_data.get("dimensions", {}).items():
        dimensions_str += f"- {dim_name}: {dim_info.get('score', 0)}分（{dim_info.get('level', '未知')}）- {dim_info.get('description', '')}\n"

    followers = account_info.get("followers", 0)
    total_posts = stats.get("total_posts", 0)
    avg_views = stats.get("avg_views", 0)

    # 分析内容类型分布
    type_counts = {}
    for p in posts:
        ct = p.get("content_type", "未分类")
        type_counts[ct] = type_counts.get(ct, 0) + 1
    type_str = "\n".join([f"  - {k}: {v}篇" for k, v in type_counts.items()])

    user_prompt = f"""请为以下小红书账号生成全面的健康度诊断报告：

📌 账号：{account_info.get('nickname', '未设置')}
📌 粉丝：{followers}
📌 累计笔记：{total_posts}
📌 平均浏览：{avg_views}

📊 健康度评分：{health_data.get('overall_score', 0)}/100（{health_data.get('level', '未知')}）

📊 各维度得分：
{dimensions_str}

📊 内容类型分布：
{type_str}

请输出完整诊断报告：

【🏥 诊断结论】
（一句话总结账号当前状态）

【📊 各项体检结果】
（逐一分析每个维度的得分，指出问题和亮点）

【🔍 核心问题诊断】
（目前最需要解决的1-2个关键问题）

【💊 处方·具体行动】
（针对每个问题给出具体的解决方案，按优先级排列）

【📈 30天改善计划】
（一个可执行的30天改善计划，每周做什么）

【⚡ 今天就做】
（诊断完立刻可以执行的1件事）"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n你是一位资深的社交媒体运营诊断师。你的诊断报告要像医生的体检报告一样：精准、有数据支撑、有具体的治疗方案。不说空话，每条建议都必须可执行。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            max_tokens=2500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"诊断失败: {str(e)}"


def generate_hot_topic_package(
    topic_desc: str,
    urgency: str = "今天发",
) -> str:
    """
    热点快反：输入一个热点话题，一键生成完整的内容包
    （标题+正文+标签+Prompt+封面建议）
    """
    user_prompt = f"""有一个热点话题需要快速出内容，请帮我一键生成完整的小红书内容包：

🔥 热点描述：{topic_desc}
⏰ 紧急程度：{urgency}
🎨 账号定位：AI油画·当代艺术

请生成以下全套内容：

【🎯 热点切入角度】
（如何把这个热点和「AI油画·当代艺术」领域结合？给出最佳切入角度）

【📌 标题（3个选择）】
（3个不同风格的标题，标注推荐度）

【✍️ 完整正文】
（500-800字的完整小红书笔记，可以直接复制使用）

【🏷️ 标签组合】
（10个标签，包含热点标签+领域标签）

【🎨 AI绘画Prompt】
（1-2个配套的Midjourney Prompt，用于生成热点相关的AI油画）

【🖼️ 封面建议】
（封面怎么做？文字放什么？）

【⏰ 发布建议】
（什么时间发？发布后要做什么？）

【💡 蹭热点技巧】
（这个热点还能怎么用？能做成系列吗？）"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n" + PROMPT_EXPERT + "\n你同时是一位反应极快的热点运营专家。你能在最短时间内把任何热点和艺术领域结合，产出高质量的蹭热点内容。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=3500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"


def generate_engagement_batch(
    scenario: str,
    keywords: list,
    count: int = 5,
) -> str:
    """
    批量生成互动巡逻用的评论（按场景+关键词定制）
    """
    keywords_str = "、".join(keywords) if keywords else "油画、当代艺术、AI绘画"

    user_prompt = f"""我要在小红书进行每日互动巡逻，请为以下场景批量生成{count}条可直接使用的评论：

📌 互动场景：{scenario}
📌 目标笔记的关键词领域：{keywords_str}
📌 我的账号定位：AI油画·当代艺术

要求：
1. 每条评论80-150字，有实质内容，不是水评论
2. 要展示「AI油画+当代艺术」的专业度
3. 每条评论的切入角度不同
4. 语气要自然真诚，不像AI写的
5. 评论里要有「留钩子」——让看到的人想点进你主页

请按以下格式输出每条评论：

【评论{i} · {角度标签}】
{评论内容}
📎 适用场景：{什么类型的笔记下面用这条}
🎣 钩子效果：{这条评论怎么引流的}"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "你是一位精通当代艺术和AI绘画的专业人士。你在小红书评论区的身份是一个懂行、有趣、热心分享的艺术爱好者。每条评论都要像真人在自然地分享观点，同时巧妙展示你的专业度。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.85,
            max_tokens=2500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"


def generate_reply_suggestions(comments: str) -> str:
    """
    为收到的评论生成高质量回复建议
    """
    user_prompt = f"""我的小红书笔记收到了以下评论，请帮我生成高质量的回复：

📌 账号定位：AI油画·当代艺术
📌 收到的评论：
{comments}

为每条评论生成回复，要求：
1. 每条回复50-100字
2. 要有「温度」——让粉丝感觉被重视
3. 回复里要包含一个「二次互动钩子」（让对方继续回复你）
4. 适当展示专业知识
5. 如果对方提了问题，要认真回答
6. 如果是夸奖，不要只说谢谢，要给出有价值的补充信息

请直接输出每条回复，标注对应的原评论。"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "你是一位有温度、有专业度的小红书艺术博主。回复评论时要真诚、有料、能引发二次互动。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.75,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"


def generate_cover_package(
    content_type: str,
    topic: str,
    title: str = "",
    style_ref: str = "",
    tool: str = "Midjourney",
) -> str:
    """
    生成完整的封面制作方案：AI绘画Prompt + Canva排版指导 + 标题文案
    目标：CTR从6%提升到8%+
    """
    from .config import COVER_TEMPLATES, COVER_UNIVERSAL_RULES, LEARNED_VIRAL_PATTERNS

    template = COVER_TEMPLATES.get(content_type, COVER_TEMPLATES.get("AI油画合集"))
    rules = COVER_UNIVERSAL_RULES
    patterns = LEARNED_VIRAL_PATTERNS

    # 构建竞品爆款经验参考
    cover_patterns = patterns.get("封面规律", {})
    title_patterns = patterns.get("标题规律", {})
    color_insight = patterns.get("色彩规律", {})

    learned_str = "【从竞品Top10爆款中学到的规律】\n"
    for p in cover_patterns.values():
        learned_str += f"- {p['name']}：{p['evidence']}（我们可以：{p['for_ai_account']}）\n"
    for p in title_patterns.values():
        learned_str += f"- {p['name']}：{p['evidence']}（适用：{p['applicable']}）\n"
    learned_str += f"- 色彩规律：{color_insight.get('insight', '')}（Prompt用：{color_insight.get('for_prompts', '')}）\n"

    user_prompt = f"""请为以下小红书笔记生成完整的封面制作方案。目标是让封面点击率(CTR)达到8%以上。

📌 内容类型：{content_type}
📌 笔记主题：{topic}
📌 已有标题（可优化）：{title if title else '请推荐'}
📌 风格参考：{style_ref if style_ref else '由你根据主题推荐'}
📌 AI绘画工具：{tool}

📋 封面模板参考：
- 布局：{template['layout']}
- 标题公式：{template['title_formula']}
- 标题示例：{'; '.join(template['title_examples'])}

📋 封面通用规则：
- 尺寸：{rules['dimensions']}
- 字体：{rules['title_font']}
- 标题位置：{rules['title_position']}
- 缩略图测试：{rules['thumbnail_test']}

{learned_str}

请按以下格式完整输出：

【🖼️ 封面AI绘画Prompt（直接复制到{tool}）】

Prompt 1（主推·最鲜艳抢眼）：
（完整英文Prompt，针对封面用途优化：高饱和度、构图留底部文字空间、3:4竖版）

Prompt 2（备选·不同构图）：
（完整英文Prompt，换一种构图/色调）

Prompt 3（备选·更暗调戏剧感）：
（完整英文Prompt，暗调风格，适合加白色标题文字）

【📝 封面标题文案（5个选择）】
（5个优化后的标题，每个≤20字，必须包含：
 ① 数字或具体描述
 ② 1个搜索关键词（AI油画/当代艺术/Midjourney/油画教程等）
 ③ 1个情感钩子（惊艳/治愈/震撼等）
 ④ 1个emoji
 标注每个标题的预估CTR效果：★★★/★★★★/★★★★★）

【🎨 Canva排版步骤（小白也能做）】
（一步一步教怎么在Canva里做封面：
 1. 尺寸设置
 2. 图片上传和铺满
 3. 滤镜/调色建议
 4. 文字添加（字体/字号/颜色/位置/阴影）
 5. 最终检查清单）

【📱 缩略图自查清单】
（做完后必须检查的5项，确保在手机小图下也能抓住眼球）

【💡 CTR提升技巧（针对这个选题）】
（3个针对性建议，帮助从6%→8%+）"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": PROMPT_EXPERT + "\n\n你同时是一位精通小红书封面设计和CTR优化的视觉营销专家。你深知：封面CTR≥8%才能突破初始流量池（200-500曝光→5000+曝光）。你的封面Prompt要针对小红书信息流缩略图场景优化：高饱和度、视觉焦点明确、底部留文字空间。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=3500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"


def generate_compliance_check(title: str, content: str, hashtags: str = "", is_ai_content: bool = True) -> str:
    """
    AI合规自查：检查内容是否触碰平台红线，并给出修改建议
    """
    user_prompt = f"""请作为小红书平台合规审核专家，对以下即将发布的笔记进行全面合规自查：

📌 标题：{title}
📌 正文：
{content}
📌 标签：{hashtags}
📌 是否使用AI工具创作：{'是' if is_ai_content else '否'}

请逐条检查以下平台红线规则，给出自查结果：

【1. 关键词堆砌检查】
- 标题中是否有关键词重复≥3次？
- 正文中是否有关键词密度过高（＞3%）？
- 标签是否与内容高度相关？
- 🟢通过 / 🔴违规 → 具体问题 + 修改建议

【2. 原创度检查】
- 内容是否像搬运/洗稿？
- 是否有明显的模板痕迹？
- 是否与常见爆款内容高度雷同？
- 🟢通过 / 🟡需改进 / 🔴违规 → 修改建议

【3. AI内容标注检查】
- 是否需要标注「AI辅助创作」？
- 图片是否为AI生成？需要说明吗？
- 🟢通过 / 🔴需标注 → 标注方式建议

【4. 绝对化用语检查】
- 是否包含「最」「第一」「100%」「根治」等禁词？
- 是否有夸大表述？
- 🟢通过 / 🔴违规 → 具体违规词 + 替代建议

【5. 商业导流检查】
- 是否包含微信号/二维码/外链？
- 是否有露骨的导流话术？
- 🟢通过 / 🔴违规 → 修改建议

【6. 互动引导检查】
- 互动引导是否合规？
- 是否有诱导关注/收藏的违规话术？
- 🟢通过 / 🟡可优化 → 建议

【7. 搜索SEO检查】
- 标题是否包含精准搜索关键词？
- 关键词是否自然融入不生硬？
- 是否覆盖了用户真实搜索意图？
- 搜索页占30%流量，这篇笔记能被搜到吗？
- → 优化后的关键词建议

【📊 合规评分：__/100】

【✅ 通过项清单】

【🔴 必须修改项（不改不能发）】

【🟡 建议优化项（改了效果更好）】

【📝 修改后的标题建议（3个）】
（确保包含搜索关键词+不触碰红线+吸引点击）

【📝 需要修改的正文段落】
（只列出需要改的部分，给出修改后版本）"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "你是一位精通小红书2025-2026年最新平台规则的合规审核专家。你对关键词堆砌、AI内容标注、绝对化用语、商业导流等违规行为有深入了解。你的检查要严格但有建设性，不仅指出问题还要给出可直接使用的修改版本。同时你也精通小红书SEO，能帮助优化搜索关键词。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=3500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"合规检查失败: {str(e)}"


def generate_funnel_diagnosis(
    funnel_results: list,
    bottleneck: dict,
    account_info: dict,
    comparison: dict = None,
) -> str:
    """
    AI深度诊断后链路漏斗数据，给出系统性优化方案
    """
    # 格式化各环节数据
    stages_str = ""
    for r in funnel_results:
        stages_str += (
            f"- {r['name']}：{r['from_label']}{r['from_value']} → {r['to_label']}{r['to_value']}，"
            f"转化率{r['rate']}%（基准线{r['benchmark_good']}%）{r['level_label']}\n"
        )

    bottleneck_str = ""
    if bottleneck:
        bottleneck_str = (
            f"最大瓶颈：{bottleneck['name']}，转化率{bottleneck['rate']}%"
            f"（基准{bottleneck['benchmark_good']}%），"
            f"原因推测：{bottleneck.get('diagnosis', '')}"
        )

    comparison_str = ""
    if comparison and comparison.get("has_comparison"):
        for c in comparison.get("changes", []):
            comparison_str += f"- {c['name']}：{c['previous_rate']}% → {c['current_rate']}%（{c['direction']} {c['delta']:+.2f}%）\n"

    followers = account_info.get("followers", 0)
    nickname = account_info.get("nickname", "未设置")

    user_prompt = f"""请对以下小红书账号的「后链路漏斗数据」进行深度诊断，给出系统性优化方案：

📌 账号：{nickname}（{followers}粉丝）
📌 领域：AI油画·当代艺术

📊 各环节转化率：
{stages_str}

🔴 最大瓶颈：
{bottleneck_str}

{'📈 对比上次变化：' + chr(10) + comparison_str if comparison_str else '（首次录入，无历史对比）'}

请按以下结构输出诊断报告：

【🔍 漏斗整体诊断】
（用一段话概括整个漏斗的健康程度。哪些环节是优势？哪些是短板？整体的「流量效率」如何？）

【🔴 瓶颈深度分析】
（对最大瓶颈环节进行深度分析：
 - 为什么这个环节转化率低？列出3个可能的具体原因
 - 这个瓶颈对下游的连锁影响是什么？
 - 解决这个瓶颈预计能带来多大的整体提升？）

【💊 优化处方·按优先级】
（给出5-8个具体的优化动作，按「投入产出比」从高到低排列：
 每个动作包含：
 - 具体做什么（精确到步骤）
 - 预计需要多长时间
 - 预计能提升哪个指标多少
 - 验证方法：怎么判断有没有效果）

【📊 分环节优化建议】
（对每个还有提升空间的环节，给出1-2个具体建议）

【📅 7天优化计划】
（一个可执行的7天计划：每天做什么来优化最大瓶颈）

【⚡ 今天就做的1件事】
（最高投入产出比的一件事，立刻可以执行）"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n你同时是一位资深的小红书增长黑客和数据分析师。你精通用户行为漏斗分析，能从转化率数据中精准定位问题并给出可量化的优化方案。每条建议必须具体到可执行的步骤，不说空话。"},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            max_tokens=3500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"诊断失败: {str(e)}"


def _parse_content(raw: str) -> dict:
    """解析AI生成的内容为结构化数据"""
    result = {
        "title": "",
        "cover_text": "",
        "body": "",
        "hashtags": [],
        "cover_suggestion": ""
    }

    sections = raw.split("【")
    for section in sections:
        if section.startswith("标题】"):
            result["title"] = section.replace("标题】", "").strip().split("\n")[0].strip()
        elif section.startswith("封面大字建议】"):
            result["cover_text"] = section.replace("封面大字建议】", "").strip()
        elif section.startswith("正文】"):
            result["body"] = section.replace("正文】", "").strip()
        elif section.startswith("话题标签】"):
            tags_text = section.replace("话题标签】", "").strip()
            result["hashtags"] = [
                tag.strip() for tag in tags_text.split("\n")
                if tag.strip() and "#" in tag
            ]
        elif section.startswith("配图建议】") or section.startswith("封面建议】"):
            key = "配图建议】" if section.startswith("配图建议】") else "封面建议】"
            result["cover_suggestion"] = section.replace(key, "").strip()
        elif section.startswith("图片排列建议】"):
            result["cover_suggestion"] = section.replace("图片排列建议】", "").strip()
        elif section.startswith("发布时间建议】"):
            result["publish_time_tip"] = section.replace("发布时间建议】", "").strip()

    # 如果有专门的封面大字建议，追加到配图建议中以防丢失
    if result["cover_text"] and "封面大字" not in result["cover_suggestion"]:
        result["cover_suggestion"] = f"【封面必须加的大字】：{result['cover_text']}\n\n" + result["cover_suggestion"]

    return result
