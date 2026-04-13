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



def render_review():
    st.markdown("## 📊 数据复盘·策略调整")
    st.markdown("_把创作者中心的数据填进来，我告诉你哪里要调整_")
    account = get_account_info()
    stats = get_overall_stats()
    adaptive = get_adaptive_tool_profile()
    latest_review = get_latest_review_snapshot()
    latest_ops = get_latest_operations_snapshot()

    tab_review, tab_ops, tab_changes, tab_plan, tab_history = st.tabs(
        ["📊 周复盘", "📈 运营面板快照", "🕓 数据变化", "🗺️ 阶段目标", "📋 历史复盘"]
    )

    with tab_review:
        st.markdown("### 📊 录入本周创作者中心数据")
        st.markdown("_每周日录入一次，对比目标，调整下周内容_")
        if adaptive.get("weekly_update_note"):
            st.markdown(f"""<div class="plan-card">{adaptive['weekly_update_note']}</div>""", unsafe_allow_html=True)
        latest_review_summary = _summarize_review_snapshot(latest_review)
        if latest_review_summary:
            st.markdown(
                f"""<div class="plan-card"><strong>🧾 最近一次周复盘：</strong>{latest_review_summary}</div>""",
                unsafe_allow_html=True,
            )

        col1, col2 = st.columns(2)
        with col1:
            r_date = st.date_input("📅 统计截止日期", key="r_date")
            r_posts = st.number_input("📝 累计已发笔记数", min_value=0, value=stats.get("total_posts", 0), key="r_posts")
            r_followers = st.number_input("👥 当前粉丝数", min_value=0, value=account.get("followers", 0), key="r_followers")
            r_followers_gain = st.number_input("📈 本周新增粉丝", min_value=0, value=0, key="r_gain")
        with col2:
            r_views = st.number_input("👀 本周平均浏览量/篇", min_value=0, value=stats.get("avg_views", 0), key="r_views")
            r_likes = st.number_input("❤️ 本周平均点赞/篇", min_value=0, value=stats.get("avg_likes", 0), key="r_likes")
            r_saves = st.number_input("⭐ 本周平均收藏/篇", min_value=0, value=stats.get("avg_saves", 0), key="r_saves")
            r_comments = st.number_input("💬 本周平均评论/篇", min_value=0, value=stats.get("avg_comments", 0), key="r_comments")

        r_best = st.text_input("🔥 本周数据最好的笔记标题", key="r_best", placeholder="写一下哪篇数据最好")
        r_best_type = st.selectbox("🔥 那篇笔记的类型", list(CONTENT_TYPES.keys()), key="r_best_type")
        r_best_views = st.number_input("🔥 那篇的浏览量", min_value=0, value=0, key="r_best_views")

        if st.button("📊 提交并获取评估", type="primary", use_container_width=True, key="submit_review"):
            review_data = {
                "date": r_date.isoformat(),
                "total_posts": r_posts,
                "followers": r_followers,
                "followers_gain": r_followers_gain,
                "avg_views": r_views,
                "avg_likes": r_likes,
                "avg_saves": r_saves,
                "avg_comments": r_comments,
                "best_post": r_best,
                "best_type": r_best_type,
                "best_post_views": r_best_views,
            }

            review_id = save_review(review_data)
            result = evaluate_performance(review_data)

            st.success(f"✅ 复盘记录#{review_id}已保存")

            st.markdown(f"### 📍 当前阶段：{result['phase']}")

            overall_emoji = "🟢" if result["overall"] == "on_track" else "🔴"
            st.markdown(f"**整体状态：** {overall_emoji} {'正常推进' if result['overall'] == 'on_track' else '需要调整'}")

            st.markdown("### 📊 各指标对比目标")
            for label, score in result["scores"].items():
                status_color = "🟢" if score["status"] in ("达标", "超标") else "🟡" if score["status"] == "偏低" else "🔴"
                st.markdown(f"""
                <div class="plan-card">
                    {status_color} <strong>{label}</strong>：实际 <strong>{score['actual']}</strong> vs 目标 {score['target']}
                    （完成率 {score['ratio']}%·{score['status']}）
                </div>
                """, unsafe_allow_html=True)

            if result["adjustments"]:
                st.markdown("### 🔧 具体调整建议")
                for adj in result["adjustments"]:
                    st.markdown(f"""<div class="tip-card">{adj}</div>""", unsafe_allow_html=True)

            st.markdown("### ⚡ 下一步行动")
            for action in result["next_actions"]:
                st.markdown(f"**{action}**")

            review_changes = get_recent_metric_changes(limit=6, source_type="weekly_review")
            if review_changes:
                st.markdown("### 🕓 最近周复盘变化")
                for change in review_changes:
                    source_label, created_at, content = _format_metric_change(change)
                    st.markdown(
                        f"""<div class="plan-card"><strong>{source_label}</strong> · {created_at}<br>{content}</div>""",
                        unsafe_allow_html=True,
                    )

    with tab_ops:
        st.markdown("### 📈 录入最新运营面板快照")
        st.markdown("_把运营面板关键字段记下来，系统会同步更新最新快照和变化历史_")

        latest_ops_summary = _summarize_operations_snapshot(latest_ops)
        if latest_ops_summary:
            st.markdown(
                f"""<div class="plan-card"><strong>📌 最近一次运营快照：</strong>{latest_ops_summary}</div>""",
                unsafe_allow_html=True,
            )

        latest_period = latest_ops.get("period") or {}
        latest_metrics = latest_ops.get("metrics") or {}
        latest_sources = latest_ops.get("traffic_sources") or []
        latest_viewer_time = latest_ops.get("viewer_time") or {}
        source_lookup = {item.get("name"): item.get("percent", 0) for item in latest_sources}

        peak_window_options = ["早间", "午间", "晚间", "深夜"]
        default_peak_window = latest_viewer_time.get("peak_window", "晚间") or "晚间"
        if default_peak_window not in peak_window_options:
            peak_window_options.insert(0, default_peak_window)

        col1, col2 = st.columns(2)
        with col1:
            ops_period_start = st.text_input("📅 统计开始", value=latest_period.get("start", ""), key="ops_period_start")
            ops_views = st.number_input("👀 观看总数", min_value=0, value=int(latest_metrics.get("views", 0) or 0), key="ops_views")
            ops_viewer_followers = st.number_input(
                "👥 观看粉丝",
                min_value=0,
                value=int(latest_metrics.get("viewer_followers", 0) or 0),
                key="ops_viewer_followers",
            )
            ops_avg_watch = st.number_input(
                "⏱️ 平均观看时长（秒）",
                min_value=0.0,
                value=float(latest_metrics.get("avg_watch_seconds", 0) or 0),
                format="%.1f",
                key="ops_avg_watch",
            )
            ops_total_watch = st.number_input(
                "⌛ 总观看时长（小时）",
                min_value=0.0,
                value=float(latest_metrics.get("total_watch_hours", 0) or 0),
                format="%.1f",
                key="ops_total_watch",
            )
        with col2:
            ops_period_end = st.text_input("📅 统计结束", value=latest_period.get("end", ""), key="ops_period_end")
            ops_conversion = st.number_input(
                "🎯 转化率（%）",
                min_value=0.0,
                max_value=100.0,
                value=float(latest_metrics.get("conversion_rate", 0) or 0),
                format="%.1f",
                key="ops_conversion",
            )
            ops_home = st.number_input(
                "🏠 首页推荐占比（%）",
                min_value=0.0,
                max_value=100.0,
                value=float(source_lookup.get("首页推荐", 0) or 0),
                format="%.1f",
                key="ops_home",
            )
            ops_search = st.number_input(
                "🔎 搜索占比（%）",
                min_value=0.0,
                max_value=100.0,
                value=float(source_lookup.get("搜索", 0) or 0),
                format="%.1f",
                key="ops_search",
            )
            ops_profile = st.number_input(
                "👤 个人主页占比（%）",
                min_value=0.0,
                max_value=100.0,
                value=float(source_lookup.get("个人主页", 0) or 0),
                format="%.1f",
                key="ops_profile",
            )
            ops_other = st.number_input(
                "🧩 其他来源占比（%）",
                min_value=0.0,
                max_value=100.0,
                value=float(source_lookup.get("其他来源", 0) or 0),
                format="%.1f",
                key="ops_other",
            )

        col3, col4 = st.columns(2)
        with col3:
            ops_peak_window = st.selectbox(
                "🌆 流量高峰时段",
                peak_window_options,
                index=peak_window_options.index(default_peak_window),
                key="ops_peak_window",
            )
        with col4:
            ops_peak_label = st.text_input(
                "🕒 高峰时间标签",
                value=latest_viewer_time.get("peak_hour_label", ""),
                key="ops_peak_label",
            )

        if st.button("💾 保存运营面板快照", type="primary", use_container_width=True, key="submit_ops_snapshot"):
            snapshot_data = {
                "period": {
                    "start": ops_period_start,
                    "end": ops_period_end,
                },
                "metrics": {
                    "views": int(ops_views),
                    "viewer_followers": int(ops_viewer_followers),
                    "avg_watch_seconds": float(ops_avg_watch),
                    "total_watch_hours": float(ops_total_watch),
                    "conversion_rate": float(ops_conversion),
                },
                "traffic_sources": [
                    {"name": "首页推荐", "percent": float(ops_home)},
                    {"name": "搜索", "percent": float(ops_search)},
                    {"name": "个人主页", "percent": float(ops_profile)},
                    {"name": "其他来源", "percent": float(ops_other)},
                ],
                "viewer_time": {
                    "peak_window": ops_peak_window,
                    "peak_hour_label": ops_peak_label,
                },
            }
            save_operations_snapshot(snapshot_data)
            st.success("✅ 运营面板快照已保存")

            ops_changes = get_recent_metric_changes(limit=6, source_type="operations_snapshot")
            if ops_changes:
                st.markdown("### 🕓 最近运营快照变化")
                for change in ops_changes:
                    source_label, created_at, content = _format_metric_change(change)
                    st.markdown(
                        f"""<div class="plan-card"><strong>{source_label}</strong> · {created_at}<br>{content}</div>""",
                        unsafe_allow_html=True,
                    )

    with tab_changes:
        st.markdown("### 🕓 最近数据变化")
        changes = get_recent_metric_changes(limit=30)
        if not changes:
            st.info("还没有记录到数据变化。先提交一次周复盘或运营面板快照。")
        else:
            for change in changes:
                source_label, created_at, content = _format_metric_change(change)
                st.markdown(
                    f"""<div class="plan-card"><strong>{source_label}</strong> · {created_at}<br>{content}</div>""",
                    unsafe_allow_html=True,
                )

    with tab_plan:
        st.markdown("### 🗺️ 12周成长计划")
        st.markdown("_从当前阶段走到1000粉的4个阶段，每个阶段的目标和内容配比_")

        current_followers = account.get("followers", 0) if account else 0
        current_posts = get_overall_stats().get("total_posts", 0)
        current_phase = get_current_phase(current_posts, current_followers)

        for phase in PHASE_TARGETS:
            is_current = phase["phase"] == current_phase["phase"]
            icon = "🔥" if is_current else "📌"

            with st.expander(
                f"{icon} {phase['phase']}{'  ← 你在这里' if is_current else ''}",
                expanded=is_current
            ):
                st.markdown(f"**周期：** {phase['duration']}")
                st.markdown(f"**内容目标：** {phase['content_target']}")
                st.markdown(f"**核心策略：** {phase['focus']}")

                st.markdown("**量化目标：**")
                t = phase["targets"]
                cols = st.columns(3)
                with cols[0]:
                    st.metric("累计笔记", t["total_posts"])
                    st.metric("平均浏览", t["avg_views"])
                with cols[1]:
                    st.metric("平均点赞", t["avg_likes"])
                    st.metric("平均收藏", t["avg_saves"])
                with cols[2]:
                    st.metric("涨粉目标", t["followers_gain"])
                    st.metric("单篇最高浏览", t["best_post_views"])

                st.markdown("**内容配比：**")
                for item in phase["content_mix"]:
                    st.markdown(f"- {item}")

    with tab_history:
        st.markdown("### 📋 历史复盘记录")
        reviews = get_all_reviews()
        if not reviews:
            st.info("暂无复盘记录。每周日在「周复盘」Tab中提交一次创作者中心数据。")
        else:
            for review_item in reversed(reviews):
                with st.expander(f"📊 #{review_item['review_id']} · {review_item.get('date', '未知日期')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("粉丝", review_item.get("followers", 0))
                        st.metric("平均浏览", review_item.get("avg_views", 0))
                        st.metric("平均点赞", review_item.get("avg_likes", 0))
                    with col2:
                        st.metric("累计笔记", review_item.get("total_posts", 0))
                        st.metric("平均收藏", review_item.get("avg_saves", 0))
                        st.metric("本周涨粉", review_item.get("followers_gain", 0))
                    if review_item.get("best_post"):
                        st.markdown(f"🔥 最佳笔记：{review_item['best_post']}（{review_item.get('best_type', '')}）")


# ==================== 页面：运营仪表盘 ====================



def _summarize_review_snapshot(review_snapshot):
    if not review_snapshot:
        return ""

    summary_parts = []
    if review_snapshot.get("followers"):
        summary_parts.append(f"粉丝 {int(review_snapshot['followers']):,}")
    if review_snapshot.get("followers_gain"):
        summary_parts.append(f"本周涨粉 {int(review_snapshot['followers_gain']):,}")
    if review_snapshot.get("avg_views"):
        summary_parts.append(f"平均浏览 {int(review_snapshot['avg_views']):,}")
    if review_snapshot.get("avg_likes"):
        summary_parts.append(f"平均点赞 {int(review_snapshot['avg_likes']):,}")
    if review_snapshot.get("best_type"):
        summary_parts.append(f"最佳类型 {review_snapshot['best_type']}")
    if review_snapshot.get("best_post_views"):
        summary_parts.append(f"最佳笔记 {int(review_snapshot['best_post_views']):,} 浏览")
    return "｜".join(summary_parts)





def _summarize_operations_snapshot(snapshot):
    if not snapshot:
        return ""

    metrics = snapshot.get("metrics") or {}
    sources = snapshot.get("traffic_sources") or []
    viewer_time = snapshot.get("viewer_time") or {}
    summary_parts = []

    if metrics.get("views"):
        summary_parts.append(f"观看 {int(metrics['views']):,}")
    if metrics.get("viewer_followers"):
        summary_parts.append(f"观看粉丝 {int(metrics['viewer_followers']):,}")
    if metrics.get("avg_watch_seconds"):
        summary_parts.append(f"平均观看 {int(metrics['avg_watch_seconds'])} 秒")
    if metrics.get("conversion_rate") is not None:
        summary_parts.append(f"转化率 {metrics.get('conversion_rate', 0)}%")
    if sources:
        primary_source = sources[0]
        if primary_source.get("name"):
            summary_parts.append(f"{primary_source['name']} {primary_source.get('percent', 0)}%")
    if viewer_time.get("peak_hour_label"):
        summary_parts.append(f"高峰 {viewer_time['peak_hour_label']}")
    return "｜".join(summary_parts)





def _format_metric_change(change):
    source_label = "周复盘" if change.get("source_type") == "weekly_review" else "运营快照"
    created_at = (change.get("created_at") or "").replace("T", " ")[:16]
    old_value = change.get("old_value")
    new_value = change.get("new_value")
    old_text = old_value if old_value not in (None, "") else "空"
    new_text = new_value if new_value not in (None, "") else "空"
    content = f"{change.get('metric_label', change.get('metric_key', '指标'))}：{old_text} -> {new_text}"
    return source_label, created_at, content


# ==================== 页面：数据复盘 ====================


