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



def render_settings():
    st.markdown("## ⚙️ 设置")

    tab1, tab2 = st.tabs(["👤 账号信息", "🔑 API配置"])

    with tab1:
        st.markdown("### 账号基本信息")
        account = get_account_info()

        nickname = st.text_input("昵称", value=account.get("nickname", ""), key="s_nick",
                                 placeholder="你的小红书昵称")
        category = st.selectbox(
            "内容领域",
            CONTENT_CATEGORIES,
            index=CONTENT_CATEGORIES.index(account.get("category", "画家故事"))
            if account.get("category") in CONTENT_CATEGORIES else 0,
            key="s_cat"
        )
        followers = st.number_input(
            "当前粉丝数",
            min_value=0,
            value=account.get("followers", 0),
            key="s_followers"
        )
        bio = st.text_area("账号简介", value=account.get("bio", ""),
                           placeholder="例如：把名画讲成故事，把油画做成可复制的审美体验",
                           key="s_bio")
        target = st.text_input(
            "运营目标",
            value=account.get("target", ""),
            placeholder="例如：3个月涨粉1000，打透经典游戏IP真人化赛道",
            key="s_target"
        )

        if st.button("💾 保存账号信息", type="primary", key="s_save"):
            save_account_info({
                "nickname": nickname,
                "category": category,
                "followers": followers,
                "bio": bio,
                "target": target,
            })
            st.success("✅ 账号信息已保存！")
            st.rerun()

    with tab2:
        st.markdown("### API 配置")
        status_label = "🟢 已启用" if ai_enabled() else "🟠 未启用"
        st.markdown(f"**当前状态：** {status_label}")
        st.info("""
        本工具使用 Claude / Anthropic API 来驱动 AI 内容生成功能。

        **配置方式（任选其一）：**
        1. 在下方填写 Claude API Key（仅本次会话有效）
        2. 在项目根目录写入 `.env.local`
        3. 设置环境变量：`CLAUDE_CODE_API_KEY` 或 `ANTHROPIC_API_KEY`
        4. 如需代理/中转，可额外设置：`CLAUDE_BASE_URL` / `ANTHROPIC_BASE_URL` / `CLAUDE_MODEL`
        """)
        st.caption("默认模型已设为 `claude-sonnet-4-6`。如使用 `.env.local`，重启应用后会自动生效。")

        new_key = st.text_input("Claude API Key", value=cfg.CLAUDE_API_KEY, type="password", key="s_api_key")
        new_url = st.text_input("Claude Base URL", value=cfg.CLAUDE_BASE_URL, key="s_api_url")
        new_model = st.text_input("模型名称", value=cfg.CLAUDE_MODEL, key="s_model")

        if st.button("💾 保存API配置", type="primary", key="s_api_save"):
            cfg.set_ai_runtime_config(new_key, new_url, new_model)
            st.success("✅ Claude API 配置已保存（本次会话有效）！")
            st.rerun()


# ==================== 主程序 ====================


