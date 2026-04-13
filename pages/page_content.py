"""Auto-extracted page module from app.py refactoring."""

import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import subprocess
import sys
from pathlib import Path

import xhs_agent.config as cfg
from pages.shared_runtime import OPENAI_API_KEY, AI_SETUP_ERROR
from xhs_agent.config import (
    CONTENT_CATEGORIES, CONTENT_TYPES, ACCOUNT_NICHE, ACCOUNT_DESC,
    TOPIC_IDEAS, CONTENT_SOP, ARTIST_DATABASE,
    ENGAGEMENT_TACTICS, MONETIZATION_ROADMAP,
    COMMENT_TEMPLATES, CONTENT_REPURPOSE_MAP, VIRAL_SCORE_DIMENSIONS,
    POST_CHECKPOINTS, DAILY_ENGAGEMENT_QUOTA, ACCOUNT_HEALTH_DIMENSIONS,
    DAILY_TIME_BLOCKS, FUNNEL_STAGES, FUNNEL_HEALTH_BENCHMARKS,
    ALGORITHM_WEIGHTS, TRAFFIC_POOL_MODEL, CREDIT_SCORE_RULES,
    PLATFORM_RED_LINES, CONTENT_GOLDEN_RULES,
    COVER_TEMPLATES, COVER_UNIVERSAL_RULES,
    AUDIENCE_PERSONA,
)
from xhs_agent.strategy import (
    get_current_stage, get_today_posting_times, get_weekly_plan,
    get_optimization_tips, get_title_formulas, get_hashtag_strategy
)
from xhs_agent.content import (
    generate_content, generate_titles, generate_hashtags,
    polish_content, analyze_and_improve,
    generate_art_prompt, generate_style_prompt, generate_batch_prompts,
    generate_post_from_result, optimize_prompt,
    analyze_viral_post, pre_publish_check, repurpose_content,
    generate_engagement_comments, analyze_competitor,
    generate_weekly_report,
    generate_morning_briefing, generate_post_performance_analysis,
    generate_account_diagnosis, generate_hot_topic_package,
    generate_engagement_batch, generate_reply_suggestions,
    generate_funnel_diagnosis, generate_compliance_check,
    generate_cover_package,
)
from xhs_agent.daily import get_today_package, get_weekly_packages
from xhs_agent.review import (
    PHASE_TARGETS, save_review, get_all_reviews,
    get_current_phase, evaluate_performance
)
from xhs_agent.tracker import (
    save_account_info, get_account_info,
    add_post_record, update_post_metrics, get_all_posts,
    get_overall_stats, get_content_type_analysis,
    get_time_analysis, get_trend_data,
    add_competitor, get_all_competitors, update_competitor,
    add_competitor_viral_post, delete_competitor,
    save_weekly_snapshot, get_weekly_snapshots,
    start_post_tracking, record_checkpoint,
    get_all_tracking, get_active_tracking, get_tracking_by_id,
    log_engagement, get_today_engagement,
    get_engagement_history, get_engagement_streak,
    calculate_account_health,
    save_funnel_record, get_all_funnel_records,
    calculate_funnel_rates, find_funnel_bottleneck,
    get_funnel_trend, get_funnel_comparison,
    calculate_algorithm_score, analyze_traffic_pool,
    extract_historical_insights, get_dynamic_benchmarks,
    get_best_performing_posts,
    save_operations_snapshot,
    get_latest_operations_snapshot,
    get_latest_review_snapshot,
    get_latest_publish_snapshot,
    get_recent_metric_changes,
    get_adaptive_tool_profile,
)


def ai_enabled() -> bool:
    return cfg.has_ai_config()


def go_to_page(page_name: str):
    st.session_state["requested_page"] = page_name



def render_topic_ideas():
    st.markdown("## 💡 选题灵感库")
    st.markdown(f"为你的「{ACCOUNT_NICHE}」账号精选的选题灵感，可在本地环境中一键生成内容。")

    for topic_category, topics in TOPIC_IDEAS.items():
        st.markdown(f"### 🎨 {topic_category}")
        cols = st.columns(2)
        for i, topic in enumerate(topics):
            with cols[i % 2]:
                st.markdown(f"""<div class="topic-card">📌 {topic}</div>""", unsafe_allow_html=True)

                if OPENAI_API_KEY:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("✍️ 生成内容", key=f"gen_{topic_category}_{i}", use_container_width=True):
                            st.session_state["quick_topic"] = topic
                            st.session_state["quick_category"] = topic_category
                    with col_b:
                        if st.button("💡 生成标题", key=f"title_{topic_category}_{i}", use_container_width=True):
                            st.session_state["quick_title_topic"] = topic
                            st.session_state["quick_title_category"] = topic_category

        st.markdown("---")

    if OPENAI_API_KEY:
        # 处理快速生成
        if st.session_state.get("quick_topic"):
            topic = st.session_state.pop("quick_topic")
            cat = st.session_state.pop("quick_category", "AI油画创作")

            # 根据选题类别匹配内容类型
            type_map = {
                "AI油画创作": "AI油画创作过程",
                "海外当代画家": "画家作品赏析",
                "色彩与技法": "色彩/构图解析",
                "艺术故事与趣闻": "画家故事/八卦",
            }
            content_type = type_map.get(cat, "画家作品赏析")

            st.markdown(f"### ✍️ 正在为「{topic}」生成内容...")
            with st.spinner("🤖 AI正在创作中..."):
                result = generate_content(cat, content_type, topic)

            if result.get("error"):
                st.error(f"生成失败: {result['error']}")
            else:
                st.success("✅ 笔记生成完成！")
                st.markdown(f"### 📌 {result['title']}")
                st.markdown(result["body"])
                if result.get("hashtags"):
                    st.markdown("### 🏷️ " + " ".join(result["hashtags"]))
                if result.get("cover_suggestion"):
                    st.markdown("### 🖼️ 配图建议")
                    st.info(result["cover_suggestion"])
                full_text = f"{result['title']}\n\n{result['body']}\n\n{' '.join(result.get('hashtags', []))}"
                st.text_area("📋 完整文案（方便复制）", full_text, height=300)

        if st.session_state.get("quick_title_topic"):
            topic = st.session_state.pop("quick_title_topic")
            cat = st.session_state.pop("quick_title_category", "AI油画创作")

            st.markdown(f"### 💡 为「{topic}」生成标题...")
            with st.spinner("🤖 正在生成标题..."):
                titles = generate_titles(cat, topic, 6)
            st.success("✅ 标题生成完成！")
            for i, title in enumerate(titles, 1):
                st.markdown(f"**{i}.** {title}")


# ==================== 页面：AI内容生成（工作流模式） ====================



def render_content_generator():
    st.markdown("## 🎨 AI内容工作流")
    st.markdown("""
    <div class="tip-card">
        <strong>📋 工作流程：</strong>
        ① Agent给你Prompt → ② 你去MJ/SD执行生成图片 → ③ 你把结果反馈回来 → ④ Agent出配套文案
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab_cover, tab3, tab4, tab5, tab6 = st.tabs([
        "🎨 Step1·出Prompt",
        "🔄 Step2·反馈出文案",
        "🖼️ 封面工坊",
        "🛠️ Prompt优化",
        "🖼️ 画家风格Prompt",
        "📦 批量出Prompt",
        "✍️ 文案工具箱",
    ])

    # ==================== Tab 1: 生成Prompt ====================
    with tab1:
        st.markdown("### 🎨 Step 1：Agent为你生成AI油画Prompt")
        st.markdown("告诉我你想画什么，我来给你专业的Prompt，你拿去MJ/SD执行")

        col1, col2 = st.columns(2)
        with col1:
            tool = st.selectbox("🛠️ 使用工具", [
                "Midjourney", "Stable Diffusion", "DALL-E 3", "ComfyUI"
            ], key="prompt_tool")
            subject = st.text_input("📌 画面主题",
                                    placeholder="例如：雨后的东京街道、窗边的猫、抽象的海洋",
                                    key="prompt_subject")
            style_ref = st.text_input("🖼️ 风格参考",
                                      placeholder="例如：Gerhard Richter / 印象派 / 厚涂肌理感",
                                      key="prompt_style")
        with col2:
            mood = st.text_input("🌈 氛围情绪",
                                 placeholder="例如：宁静忧郁 / 温暖明亮 / 戏剧性张力",
                                 key="prompt_mood")
            ar = st.selectbox("📐 宽高比", [
                "3:4 (竖版·小红书首选)", "1:1 (方形)", "4:3 (横版)",
                "9:16 (手机全屏)", "16:9 (宽屏)", "2:3"
            ], key="prompt_ar")
            extra = st.text_input("💡 额外要求",
                                  placeholder="例如：要有明显笔触 / 低饱和度 / 暗调",
                                  key="prompt_extra")

        aspect_ratio = ar.split("(")[0].strip()

        if st.button("🚀 生成Prompt", type="primary", use_container_width=True, key="gen_prompt_btn"):
            if not subject:
                st.warning("请输入画面主题")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner("🤖 正在生成专业Prompt..."):
                    result = generate_art_prompt(tool, style_ref, subject, mood, aspect_ratio, extra)
                st.success("✅ Prompt生成完成！复制下面的Prompt去执行吧")
                st.markdown(result)

    # ==================== Tab 2: 反馈结果 → 生成文案 ====================
    with tab2:
        st.markdown("### 🔄 Step 2：你执行完了？告诉我结果，我来出文案")
        st.markdown("""
        <div class="tip-card">
            你用Prompt生成好图片后，在下面描述一下结果，我帮你写配套的小红书文案。
        </div>
        """, unsafe_allow_html=True)

        result_desc = st.text_area("📝 描述你的生成结果",
                                   height=120,
                                   placeholder="例如：\n"
                                   "用MJ生成了4张图，模仿Richter的风格画了雨后街道\n"
                                   "第2张和第4张效果最好，色调偏冷，有模糊的光影效果\n"
                                   "整体感觉很有氛围感，笔触效果比较明显",
                                   key="result_desc")
        orig_prompt = st.text_area("📋 使用的Prompt（可选，填了会让文案更准确）",
                                   height=80,
                                   placeholder="粘贴你执行时用的英文Prompt...",
                                   key="orig_prompt")

        col1, col2 = st.columns(2)
        with col1:
            post_type = st.selectbox("📋 要做成什么类型的笔记", list(CONTENT_TYPES.keys()), key="post_type")
        with col2:
            post_style = st.selectbox("🎨 文案风格", [
                "文艺有品", "专业深度", "轻松科普", "故事感强",
                "活泼有趣", "冷静理性", "热情安利"
            ], key="post_style")

        if st.button("✍️ 生成配套文案", type="primary", use_container_width=True, key="gen_post_btn"):
            if not result_desc:
                st.warning("请描述一下你的生成结果")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner("🤖 正在为你的作品写配套文案..."):
                    result = generate_post_from_result(result_desc, orig_prompt, post_type, post_style)

                if result.get("error"):
                    st.error(f"生成失败: {result['error']}")
                else:
                    st.success("✅ 配套文案生成完成！")

                    st.markdown(f"### 📌 {result['title']}")
                    st.markdown(result["body"])

                    if result.get("hashtags"):
                        st.markdown("### 🏷️ " + " ".join(result["hashtags"]))

                    if result.get("cover_suggestion"):
                        st.markdown("### 🖼️ 图片排列建议")
                        st.info(result["cover_suggestion"])

                    if result.get("publish_time_tip"):
                        st.markdown("### ⏰ 发布时间建议")
                        st.info(result["publish_time_tip"])

                    full_text = f"{result['title']}\n\n{result['body']}\n\n{' '.join(result.get('hashtags', []))}"
                    st.text_area("📋 完整文案（方便复制）", full_text, height=300, key="copy_post")

    # ==================== Tab: 封面工坊 ====================
    with tab_cover:
        st.markdown("### 🖼️ 封面工坊·CTR提升利器")
        st.markdown("""
        <div class="tip-card" style="border-left-color:#e94560">
            <strong>⚠️ 你的封面CTR=6.1%，需要≥8%才能突破流量池！</strong><br>
            封面+标题是决定用户在信息流里「点不点进来」的唯一因素。这个工坊帮你一键生成：<br>
            ① AI封面图Prompt（高饱和度+留文字空间） ② 标题文案（5选1） ③ Canva排版教程
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            cv_type = st.selectbox("📋 内容类型", list(COVER_TEMPLATES.keys()), key="cv_type")
            cv_topic = st.text_input("📌 笔记主题",
                                      placeholder="例如：莫兰迪色油画合集 / Richter模糊画法",
                                      key="cv_topic")
        with col2:
            cv_title = st.text_input("📝 已有标题（可选，AI会帮你优化）",
                                      placeholder="例如：用AI画了一组莫兰迪色油画",
                                      key="cv_title")
            cv_tool = st.selectbox("🛠️ AI绘画工具", [
                "Midjourney", "Stable Diffusion", "DALL-E 3"
            ], key="cv_tool")

        cv_style = st.text_input("🎨 风格参考（可选）",
                                  placeholder="例如：高饱和度暖色调 / Richter模糊风 / 莫兰迪灰调",
                                  key="cv_style")

        # 显示当前类型的封面模板
        template = COVER_TEMPLATES.get(cv_type, {})
        with st.expander(f"📋 「{cv_type}」封面模板参考", expanded=False):
            st.markdown(f"**布局：** {template.get('layout', '')}")
            st.markdown(f"**标题公式：** `{template.get('title_formula', '')}`")
            st.markdown("**标题示例：**")
            for ex in template.get("title_examples", []):
                st.markdown(f"- {ex}")
            st.markdown("**设计规则：**")
            for rule in template.get("design_rules", []):
                st.markdown(f"- {rule}")

        if st.button("🖼️ 生成完整封面方案", type="primary", use_container_width=True, key="gen_cover_btn"):
            if not cv_topic:
                st.warning("请输入笔记主题")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner("🤖 正在生成封面方案（Prompt+标题+排版教程）..."):
                    result = generate_cover_package(cv_type, cv_topic, cv_title, cv_style, cv_tool)
                st.success("✅ 封面方案生成完成！按步骤执行")
                st.markdown(result)

        # 通用规则速查
        st.markdown("---")
        st.markdown("### 📏 封面通用规则速查")
        rules = COVER_UNIVERSAL_RULES
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown(f"**📐 尺寸：** {rules['dimensions']}")
            st.markdown(f"**🔤 字体：** {rules['title_font']}")
            st.markdown(f"**🎨 颜色：** {rules['title_color']}")
            st.markdown(f"**📍 位置：** {rules['title_position']}")
        with col_r2:
            st.markdown(f"**📱 自查：** {rules['thumbnail_test']}")
            st.markdown("**🎨 配色要点：**")
            for cr in rules["color_rules"]:
                st.markdown(f"- {cr}")

        st.markdown("**❌ 绝对不要做的事：**")
        for dont in rules["absolute_donts"]:
            st.markdown(f"  {dont}")

    # ==================== Tab 3: Prompt优化 ====================
    with tab3:
        st.markdown("### 🛠️ 效果不满意？帮你优化Prompt")
        st.markdown("把你用过的Prompt和不满意的地方告诉我，我来调整")

        bad_prompt = st.text_area("📋 你用过的Prompt",
                                  height=100,
                                  placeholder="粘贴效果不好的Prompt...",
                                  key="bad_prompt")
        issue = st.text_area("❌ 哪里不满意",
                             height=80,
                             placeholder="例如：颜色太鲜艳了不像油画 / 构图太满 / 没有笔触感 / 人脸变形...",
                             key="prompt_issue")

        if st.button("🔧 优化Prompt", type="primary", use_container_width=True, key="fix_prompt_btn"):
            if not bad_prompt or not issue:
                st.warning("请填写Prompt和问题描述")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner("🤖 正在分析问题并优化..."):
                    fixed = optimize_prompt(bad_prompt, issue)
                st.success("✅ 优化完成！试试新的Prompt")
                st.markdown(fixed)

    # ==================== Tab 4: 画家风格Prompt ====================
    with tab4:
        st.markdown("### 🖼️ 学习画家风格的Prompt")
        st.markdown("输入画家名字，帮你拆解其视觉风格并生成可用的Prompt模板")

        col1, col2 = st.columns(2)
        with col1:
            painter = st.text_input("🎨 画家名字",
                                    placeholder="例如：Gerhard Richter / Peter Doig / Jenny Saville",
                                    key="painter_name")
        with col2:
            painter_tool = st.selectbox("🛠️ 使用工具", [
                "Midjourney", "Stable Diffusion", "DALL-E 3"
            ], key="painter_tool")

        # 快速选择常见画家
        st.markdown("**💡 快速选择：**")
        quick_painters = [
            "Gerhard Richter", "David Hockney", "Jenny Saville",
            "Peter Doig", "Cecily Brown", "Anselm Kiefer",
            "Adrian Ghenie", "Flora Yukhnovich", "Claude Monet",
        ]
        cols = st.columns(3)
        for i, p in enumerate(quick_painters):
            with cols[i % 3]:
                if st.button(p, key=f"qp_{i}", use_container_width=True):
                    st.session_state["painter_name"] = p

        if st.button("🚀 生成风格Prompt", type="primary", use_container_width=True, key="style_prompt_btn"):
            painter_val = st.session_state.get("painter_name", painter) or painter
            if not painter_val:
                st.warning("请输入画家名字")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner(f"🤖 正在分析{painter_val}的风格并生成Prompt..."):
                    result = generate_style_prompt(painter_val, painter_tool)
                st.success(f"✅ {painter_val}风格Prompt生成完成！")
                st.markdown(result)

    # ==================== Tab 5: 批量Prompt ====================
    with tab5:
        st.markdown("### 📦 批量生成一组主题Prompt")
        st.markdown("一次性生成一组风格统一的Prompt，适合做合集/系列内容")

        col1, col2 = st.columns(2)
        with col1:
            batch_theme = st.text_input("📌 系列主题",
                                        placeholder="例如：四季的森林 / 世界各地的咖啡馆 / 被遗弃的建筑",
                                        key="batch_theme")
            batch_tool = st.selectbox("🛠️ 使用工具", [
                "Midjourney", "Stable Diffusion", "DALL-E 3"
            ], key="batch_tool")
        with col2:
            batch_count = st.slider("生成数量", 3, 9, 5, key="batch_count")

        if st.button("🚀 批量生成Prompt", type="primary", use_container_width=True, key="batch_btn"):
            if not batch_theme:
                st.warning("请输入系列主题")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner(f"🤖 正在生成{batch_count}个Prompt..."):
                    result = generate_batch_prompts(batch_theme, batch_count, batch_tool)
                st.success("✅ 批量Prompt生成完成！")
                st.markdown(result)

    # ==================== Tab 6: 文案工具箱（原有功能） ====================
    with tab6:
        st.markdown("### ✍️ 文案工具箱")
        st.markdown("文字笔记生成、标题、标签、润色、分析等工具")

        sub = st.radio("选择工具", [
            "📝 生成笔记文案", "💡 批量标题", "🏷️ 标签推荐", "✨ 润色/分析"
        ], horizontal=True, key="toolbox_sub")

        if sub == "📝 生成笔记文案":
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("📂 内容分类", CONTENT_CATEGORIES, key="gen_cat")
                content_type = st.selectbox("📋 内容类型", list(CONTENT_TYPES.keys()), key="gen_type")
                topic = st.text_input("🎯 具体主题",
                                      placeholder="例如：Gerhard Richter的抽象画",
                                      key="gen_topic")
            with col2:
                keywords = st.text_input("🔑 关键词",
                                         placeholder="逗号分隔",
                                         key="gen_kw")
                style = st.selectbox("🎨 风格", [
                    "文艺有品", "专业深度", "轻松科普", "故事感强",
                ], key="gen_style")
            if st.button("🚀 生成文案", type="primary", key="gen_btn"):
                if not topic:
                    st.warning("请输入主题")
                elif not OPENAI_API_KEY:
                    st.error(AI_SETUP_ERROR)
                else:
                    with st.spinner("🤖 AI创作中..."):
                        kw_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else None
                        result = generate_content(category, content_type, topic, kw_list, style)
                    if result.get("error"):
                        st.error(f"生成失败: {result['error']}")
                    else:
                        st.success("✅ 完成！")
                        st.markdown(f"### 📌 {result['title']}")
                        st.markdown(result["body"])
                        if result.get("hashtags"):
                            st.markdown(" ".join(result["hashtags"]))
                        full_text = f"{result['title']}\n\n{result['body']}\n\n{' '.join(result.get('hashtags', []))}"
                        st.text_area("📋 复制文案", full_text, height=250, key="copy_tb")

        elif sub == "💡 批量标题":
            t_cat = st.selectbox("📂 分类", CONTENT_CATEGORIES, key="title_cat")
            t_topic = st.text_input("🎯 主题", placeholder="例如：用AI模仿莫奈", key="title_topic")
            t_count = st.slider("数量", 3, 10, 6, key="title_count")
            if st.button("🚀 生成标题", type="primary", key="title_btn"):
                if t_topic and OPENAI_API_KEY:
                    with st.spinner("🤖 生成中..."):
                        titles = generate_titles(t_cat, t_topic, t_count)
                    for i, t in enumerate(titles, 1):
                        st.markdown(f"**{i}.** {t}")

        elif sub == "🏷️ 标签推荐":
            h_cat = st.selectbox("📂 分类", CONTENT_CATEGORIES, key="hash_cat")
            h_topic = st.text_input("🎯 主题", placeholder="例如：当代油画", key="hash_topic")
            if st.button("🚀 生成标签", type="primary", key="hash_btn"):
                if h_topic and OPENAI_API_KEY:
                    with st.spinner("🤖 分析中..."):
                        tags = generate_hashtags(h_cat, h_topic)
                    st.markdown(tags)

        elif sub == "✨ 润色/分析":
            mode = st.radio("", ["✨ 润色", "🔍 分析"], horizontal=True, key="polish_mode")
            if mode == "✨ 润色":
                p_input = st.text_area("📝 粘贴内容", height=200, key="polish_input")
                if st.button("✨ 润色", type="primary", key="polish_btn"):
                    if p_input and OPENAI_API_KEY:
                        with st.spinner("🤖 润色中..."):
                            st.markdown(polish_content(p_input))
            else:
                a_t = st.text_input("📌 标题", key="analyze_title")
                a_c = st.text_area("📝 正文", height=200, key="analyze_content")
                if st.button("🔍 分析", type="primary", key="analyze_btn"):
                    if a_c and OPENAI_API_KEY:
                        with st.spinner("🤖 分析中..."):
                            st.markdown(analyze_and_improve(a_t, a_c))


# ==================== 页面：EXIF处理 ====================


