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



def render_dashboard():
    st.markdown(f"""
    <div class="main-header">
        <h1>🎨 {ACCOUNT_NICHE} 运营Agent</h1>
        <p>{ACCOUNT_DESC}</p>
    </div>
    """, unsafe_allow_html=True)

    account = get_account_info()
    adaptive = get_adaptive_tool_profile()
    followers = account.get("followers", 0) if account else 0
    stage = get_current_stage(followers)

    # 当前阶段
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        ### 📍 当前阶段：<span class="stage-badge">{stage['stage']}</span>
        **粉丝目标区间：** {stage['followers']} &nbsp;|&nbsp; **预估周期：** {stage['duration']}
        """, unsafe_allow_html=True)
    with col2:
        st.metric("当前粉丝数", f"{followers:,}", help="在设置页面更新粉丝数")

    st.markdown("---")

    # 数据概览
    stats = get_overall_stats()
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <h3>{stats['total_posts']}</h3><p>🖼️ 已发布笔记</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <h3>{stats['avg_views']:,}</h3><p>👀 平均浏览量</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <h3>{stats.get('avg_like_rate', 0)}%</h3><p>❤️ 平均点赞率</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <h3>{stats.get('avg_save_rate', 0)}%</h3><p>⭐ 平均收藏率</p>
        </div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f"""<div class="metric-card">
            <h3>{stats.get('avg_comment_rate', 0)}%</h3><p>💬 平均评论率</p>
        </div>""", unsafe_allow_html=True)

    latest_review = get_latest_review_snapshot()
    latest_review_summary = _summarize_review_snapshot(latest_review)
    if latest_review_summary:
        st.markdown(
            f"""<div class="plan-card"><strong>🧾 最新周复盘：</strong>{latest_review_summary}</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # 核心受众画像
    st.markdown("### 🎯 核心受众画像")
    st.markdown(f"""
    <div class="tip-card" style="border-left-color:#e94560;">
        <strong>📌 当前账号信号：</strong>{adaptive.get('dynamic_audience_hint', '近期更容易跑出来的是名画反差故事、画家冷知识、价格/技法解释这类内容。')}
    </div>
    """, unsafe_allow_html=True)

    aud_cols = st.columns(4)
    with aud_cols[0]:
        st.markdown(f"**👦 性别：**<br>{AUDIENCE_PERSONA['gender']}", unsafe_allow_html=True)
    with aud_cols[1]:
        st.markdown(f"**💼 年龄：**<br>{AUDIENCE_PERSONA['age']}", unsafe_allow_html=True)
    with aud_cols[2]:
        st.markdown(f"**📍 地域：**<br>{AUDIENCE_PERSONA['geography']}", unsafe_allow_html=True)
    with aud_cols[3]:
        st.markdown(f"**🎯 兴趣：**<br>{AUDIENCE_PERSONA['interests']}", unsafe_allow_html=True)

    with st.expander("📖 查看详细人群洞察与写作建议", expanded=False):
        st.markdown(f"**心理特征：** {AUDIENCE_PERSONA['psychographics']}")

    if adaptive.get("weekly_actions"):
        st.markdown("### 🗓️ 本周系统自动调整")
        for line in adaptive["weekly_actions"][:4]:
            st.markdown(f"- {line}")

    st.markdown("---")

    # 今日推荐 + 阶段任务
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ⏰ 今日最佳发布时间")
        times = get_today_posting_times()
        for t in times:
            score_bar = "🟢" if t["score"] >= 90 else "🟡" if t["score"] >= 85 else "🟠"
            st.markdown(f"""
            <div class="plan-card">
                <span class="time-badge">{t['time']}</span> &nbsp; {score_bar} 推荐指数 {t['score']}分
                <br><small style="color:#666">{t['desc']}</small>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🎯 当前阶段重点")
        for focus in stage["focus"]:
            st.markdown(f"- ✅ {focus}")

        st.markdown("### 💡 实操建议")
        for tip in stage["tips"][:4]:
            st.markdown(f"""<div class="tip-card">{tip}</div>""", unsafe_allow_html=True)
        if len(stage["tips"]) > 4:
            with st.expander("查看更多建议"):
                for tip in stage["tips"][4:]:
                    st.markdown(f"- {tip}")


# ==================== 页面：选题灵感库 ====================


