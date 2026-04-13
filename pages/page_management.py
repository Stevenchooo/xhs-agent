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



def render_post_manager():
    st.markdown("## 📝 笔记管理")

    tab1, tab2 = st.tabs(["➕ 添加笔记", "📋 笔记列表"])

    with tab1:
        st.markdown("### 记录新发布的笔记")
        col1, col2 = st.columns(2)
        with col1:
            p_title = st.text_input("📌 笔记标题", key="post_title")
            p_category = st.selectbox("📂 内容分类", CONTENT_CATEGORIES, key="post_cat")
            p_type = st.selectbox("📋 内容类型", list(CONTENT_TYPES.keys()), key="post_type")
        with col2:
            p_date = st.date_input("📅 发布日期", key="post_date")
            p_time = st.time_input("⏰ 发布时间", key="post_time")
            p_link = st.text_input("🔗 笔记链接（可选）", key="post_link")

        p_notes = st.text_area("📝 备注", height=80, key="post_notes",
                               placeholder="例如：介绍了Gerhard Richter的3幅代表作")

        st.markdown("#### 📊 初始数据（可选，发布24h后填写）")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            m_views = st.number_input("👀 浏览", min_value=0, value=0, key="m_views")
        with col2:
            m_likes = st.number_input("❤️ 点赞", min_value=0, value=0, key="m_likes")
        with col3:
            m_saves = st.number_input("⭐ 收藏", min_value=0, value=0, key="m_saves")
        with col4:
            m_comments = st.number_input("💬 评论", min_value=0, value=0, key="m_comments")
        with col5:
            m_shares = st.number_input("🔄 分享", min_value=0, value=0, key="m_shares")

        if st.button("💾 保存笔记记录", type="primary", key="save_post_btn"):
            if not p_title:
                st.warning("请输入笔记标题")
            else:
                record = {
                    "title": p_title,
                    "category": p_category,
                    "content_type": p_type,
                    "post_date": p_date.isoformat(),
                    "post_time": p_time.strftime("%H:%M"),
                    "link": p_link,
                    "notes": p_notes,
                }
                post_id = add_post_record(record)

                if any([m_views, m_likes, m_saves, m_comments, m_shares]):
                    update_post_metrics(post_id, {
                        "views": m_views,
                        "likes": m_likes,
                        "saves": m_saves,
                        "comments": m_comments,
                        "shares": m_shares,
                    })

                st.success(f"✅ 笔记已保存！ID: {post_id}")

    with tab2:
        posts = get_all_posts()
        latest_publish = get_latest_publish_snapshot()
        tracked_count = len(posts)

        if latest_publish:
            total_posts = int(latest_publish.get("total_posts", 0) or 0)
            video_posts = int(latest_publish.get("video_posts", 0) or 0)
            image_posts = int(latest_publish.get("image_posts", 0) or 0)
            missing_count = max(total_posts - tracked_count, 0)
            window = latest_publish.get("window", "近30日")
            period = latest_publish.get("period") or {}
            period_label = ""
            if period.get("start") and period.get("end"):
                period_label = f"（{period['start']} ~ {period['end']}）"

            st.markdown(f"""<div class="plan-card">
                <strong>📦 平台发文快照：</strong>{window}{period_label}<br>
                总发文 <strong>{total_posts}</strong> 条 ｜ 视频 <strong>{video_posts}</strong> ｜ 图文 <strong>{image_posts}</strong><br>
                已同步标题级明细 <strong>{tracked_count}</strong> 条
            </div>""", unsafe_allow_html=True)

            if missing_count > 0:
                st.info(f"平台近30天共发文 {total_posts} 条，但当前只同步了 {tracked_count} 条标题级明细；其余 {missing_count} 条还没有逐条标题和发布时间。")

        if not posts:
            st.info("暂无笔记记录，请先添加笔记")
        else:
            st.markdown(f"共 **{tracked_count}** 条已同步笔记记录")

            for post in reversed(posts):
                with st.expander(
                    f"#{post['id']} | {post.get('title', '无标题')} | "
                    f"{post.get('post_date', '')} {post.get('post_time', '')}"
                ):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**分类：** {post.get('category', '-')}")
                        st.markdown(f"**类型：** {post.get('content_type', '-')}")
                        if post.get("link"):
                            st.markdown(f"**链接：** {post['link']}")
                        if post.get("notes"):
                            st.markdown(f"**备注：** {post['notes']}")

                    with col2:
                        metrics = post.get("latest_metrics", {})
                        if metrics:
                            st.markdown("**最新数据：**")
                            m_cols = st.columns(5)
                            with m_cols[0]:
                                st.metric("浏览", metrics.get("views", 0))
                            with m_cols[1]:
                                st.metric("点赞", metrics.get("likes", 0))
                            with m_cols[2]:
                                st.metric("收藏", metrics.get("saves", 0))
                            with m_cols[3]:
                                st.metric("评论", metrics.get("comments", 0))
                            with m_cols[4]:
                                st.metric("分享", metrics.get("shares", 0))
                        else:
                            st.info("暂无数据记录")

                    st.markdown("---")
                    st.markdown("**📊 更新数据：**")
                    u_cols = st.columns(6)
                    with u_cols[0]:
                        u_views = st.number_input("浏览", min_value=0, key=f"u_v_{post['id']}")
                    with u_cols[1]:
                        u_likes = st.number_input("点赞", min_value=0, key=f"u_l_{post['id']}")
                    with u_cols[2]:
                        u_saves = st.number_input("收藏", min_value=0, key=f"u_s_{post['id']}")
                    with u_cols[3]:
                        u_comments = st.number_input("评论", min_value=0, key=f"u_c_{post['id']}")
                    with u_cols[4]:
                        u_shares = st.number_input("分享", min_value=0, key=f"u_sh_{post['id']}")
                    with u_cols[5]:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("更新", key=f"u_btn_{post['id']}"):
                            update_post_metrics(post["id"], {
                                "views": u_views,
                                "likes": u_likes,
                                "saves": u_saves,
                                "comments": u_comments,
                                "shares": u_shares,
                            })
                            st.success("✅ 数据已更新")
                            st.rerun()


# ==================== 页面：爆款实验室 ====================



def render_competitor():
    st.markdown("""
    <div class="main-header">
        <h1>🏆 竞品雷达</h1>
        <p>知己知彼 · 追踪竞品 · 发现差异化机会 · AI策略分析</p>
    </div>
    """, unsafe_allow_html=True)

    tab_list, tab_add, tab_analyze = st.tabs([
        "📋 竞品列表",
        "➕ 添加竞品",
        "🤖 AI竞品分析",
    ])

    # ==================== Tab 1: 竞品列表 ====================
    with tab_list:
        competitors = get_all_competitors()
        if not competitors:
            st.info("暂无竞品记录。去「➕ 添加竞品」Tab添加同赛道的竞品账号。")
            st.markdown("""
            <div class="tip-card">
                <strong>💡 怎么找竞品？</strong><br>
                在小红书搜索「油画」「当代艺术」「AI绘画」「画家推荐」等关键词，
                找到和你做同类内容、粉丝量在你的±50%~5倍范围内的博主。
                他们就是你的直接竞品。
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"共追踪 **{len(competitors)}** 个竞品账号")

            for comp in competitors:
                with st.expander(
                    f"{'🔴' if comp.get('followers', 0) > 10000 else '🟡' if comp.get('followers', 0) > 1000 else '🟢'} "
                    f"{comp.get('nickname', '未知')}（{comp.get('followers', 0):,}粉）· {comp.get('niche', '')}"
                ):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**小红书ID：** {comp.get('xhs_id', '未记录')}")
                        st.markdown(f"**领域：** {comp.get('niche', '未记录')}")
                        st.markdown(f"**内容风格：** {comp.get('content_style', '未记录')}")
                        st.markdown(f"**发布频率：** {comp.get('posting_frequency', '未记录')}")
                    with col2:
                        st.markdown(f"**核心优势：** {comp.get('strength', '未记录')}")
                        st.markdown(f"**薄弱点：** {comp.get('weakness', '未记录')}")
                        if comp.get('notes'):
                            st.markdown(f"**备注：** {comp['notes']}")

                    # 更新粉丝数
                    col_u1, col_u2 = st.columns([3, 1])
                    with col_u1:
                        new_followers = st.number_input("更新粉丝数",
                                                         min_value=0,
                                                         value=comp.get("followers", 0),
                                                         key=f"comp_f_{comp['id']}")
                    with col_u2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("更新", key=f"comp_update_{comp['id']}"):
                            update_competitor(comp["id"], {"followers": new_followers})
                            st.success("✅ 已更新")
                            st.rerun()

                    # 爆款笔记记录
                    viral = comp.get("viral_posts", [])
                    if viral:
                        st.markdown("**🔥 爆款笔记记录：**")
                        for vp in viral[-5:]:
                            st.markdown(f"- 「{vp.get('title', '')}」浏览{vp.get('views', '?')} 点赞{vp.get('likes', '?')}（{vp.get('recorded_at', '')[:10]}）")

                    st.markdown("---")
                    st.markdown("**➕ 记录TA的爆款笔记：**")
                    vp_cols = st.columns([3, 1, 1])
                    with vp_cols[0]:
                        vp_title = st.text_input("标题", key=f"vp_t_{comp['id']}", placeholder="爆款笔记标题")
                    with vp_cols[1]:
                        vp_views = st.number_input("浏览", min_value=0, key=f"vp_v_{comp['id']}")
                    with vp_cols[2]:
                        vp_likes = st.number_input("点赞", min_value=0, key=f"vp_l_{comp['id']}")

                    if st.button("记录爆款", key=f"vp_add_{comp['id']}"):
                        if vp_title:
                            add_competitor_viral_post(comp["id"], {
                                "title": vp_title,
                                "views": vp_views,
                                "likes": vp_likes,
                            })
                            st.success("✅ 爆款记录已添加")
                            st.rerun()

                    if st.button("🗑️ 删除此竞品", key=f"comp_del_{comp['id']}"):
                        delete_competitor(comp["id"])
                        st.success("✅ 已删除")
                        st.rerun()

    # ==================== Tab 2: 添加竞品 ====================
    with tab_add:
        st.markdown("### ➕ 添加竞品账号")

        col1, col2 = st.columns(2)
        with col1:
            comp_nick = st.text_input("📌 昵称", key="comp_nick", placeholder="竞品账号昵称")
            comp_xhs_id = st.text_input("🔗 小红书ID", key="comp_xhs_id", placeholder="可选")
            comp_followers = st.number_input("👥 粉丝数", min_value=0, value=0, key="comp_followers")
            comp_niche = st.text_input("🎯 领域", key="comp_niche", placeholder="例如：AI绘画 / 油画赏析 / 艺术科普")
        with col2:
            comp_style = st.text_input("🎨 内容风格", key="comp_style",
                                        placeholder="例如：专业深度型 / 轻松科普型 / 视觉震撼型")
            comp_freq = st.text_input("📅 发布频率", key="comp_freq",
                                       placeholder="例如：日更 / 每周3-4篇 / 不固定")
            comp_strength = st.text_input("💪 核心优势", key="comp_strength",
                                           placeholder="例如：图片质量极高 / 知识储备深厚")
            comp_weakness = st.text_input("⚠️ 薄弱点", key="comp_weakness",
                                           placeholder="例如：标题一般 / 互动引导弱 / 不做教程")

        comp_notes = st.text_area("📝 备注", key="comp_notes", height=80,
                                   placeholder="其他观察和想法...")

        if st.button("💾 保存竞品信息", type="primary", use_container_width=True, key="save_comp_btn"):
            if not comp_nick:
                st.warning("请输入竞品昵称")
            else:
                comp_id = add_competitor({
                    "nickname": comp_nick,
                    "xhs_id": comp_xhs_id,
                    "followers": comp_followers,
                    "niche": comp_niche,
                    "content_style": comp_style,
                    "posting_frequency": comp_freq,
                    "strength": comp_strength,
                    "weakness": comp_weakness,
                    "notes": comp_notes,
                })
                st.success(f"✅ 竞品已保存！ID: {comp_id}")

    # ==================== Tab 3: AI竞品分析 ====================
    with tab_analyze:
        st.markdown("### 🤖 AI竞品分析·差异化策略")
        st.markdown("""
        <div class="tip-card">
            <strong>用法：</strong>描述一个竞品账号的情况（内容风格、粉丝数、爆款类型等），
            AI帮你分析其优劣势，给出差异化竞争策略。也可以从竞品列表中选择。
        </div>
        """, unsafe_allow_html=True)

        # 从已有竞品选择
        competitors = get_all_competitors()
        comp_desc = ""
        if competitors:
            comp_options = ["手动输入"] + [f"{c['nickname']}（{c.get('followers', 0)}粉）" for c in competitors]
            selected = st.selectbox("📋 选择竞品（或手动输入）", comp_options, key="comp_select")
            if selected != "手动输入":
                idx = comp_options.index(selected) - 1
                comp = competitors[idx]
                comp_desc = (
                    f"昵称：{comp.get('nickname', '')}\n"
                    f"粉丝数：{comp.get('followers', 0)}\n"
                    f"领域：{comp.get('niche', '')}\n"
                    f"内容风格：{comp.get('content_style', '')}\n"
                    f"发布频率：{comp.get('posting_frequency', '')}\n"
                    f"核心优势：{comp.get('strength', '')}\n"
                    f"薄弱点：{comp.get('weakness', '')}\n"
                    f"备注：{comp.get('notes', '')}\n"
                )
                viral_str = "\n".join([f"- 「{vp.get('title', '')}」浏览{vp.get('views', '?')}" for vp in comp.get('viral_posts', [])[-5:]])
                if viral_str:
                    comp_desc += f"爆款笔记：\n{viral_str}"

        comp_input = st.text_area("📝 竞品信息描述", height=200, value=comp_desc,
                                   placeholder="描述竞品账号情况：\n- 昵称/粉丝数\n- 做什么内容\n- 什么风格\n- 发布频率\n- 最火的几篇笔记标题\n- 你观察到的优缺点",
                                   key="comp_analyze_input")

        if st.button("🤖 AI分析竞品", type="primary", use_container_width=True, key="analyze_comp_btn"):
            if not comp_input:
                st.warning("请输入竞品信息")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner("🤖 正在分析竞品并制定差异化策略..."):
                    result = analyze_competitor(comp_input)
                st.success("✅ 竞品分析完成！")
                st.markdown(result)


# ==================== 页面：晨间工作台 ====================


