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



def render_daily():
    pkg = get_today_package()
    rec = pkg.get("smart_rec", {})

    st.markdown(f"""
    <div class="main-header">
        <h1>📌 今日执行任务</h1>
        <p>{pkg['date']} {pkg['weekday']}｜今天发：{pkg['type']}｜建议 {pkg.get('time', '21:00')} 发布</p>
    </div>
    """, unsafe_allow_html=True)

    # 智能上下文信息
    if rec:
        season = rec.get("season", {})
        upcoming = rec.get("upcoming_events", [])

        context_parts = [f"📍 当前季节：**{season.get('name', '')}**（推荐色调：{season.get('colors', '')}）"]

        week_strat = rec.get("week_strategy", {})
        if week_strat.get("mood"):
            context_parts.append(f"📅 {pkg['weekday']}用户心态：{week_strat['mood']}")
        if week_strat.get("avoid"):
            context_parts.append(f"⚠️ {week_strat['avoid']}")

        st.markdown(f"""<div class="plan-card">{'<br>'.join(context_parts)}</div>""", unsafe_allow_html=True)

        # 节日提醒
        if upcoming:
            upcoming_str = " · ".join([f"**{e['date']} {e['name']}**（{e['heat']}）" for e in upcoming[:3]])
            st.markdown(f"""<div class="tip-card">🔮 未来7天节日提醒：{upcoming_str}<br><small>节日前1天准备内容，节日当天发布，蹭热点流量翻2-3倍</small></div>""", unsafe_allow_html=True)

    # 今日主题
    st.markdown(f"### 🎯 今日主题：{pkg.get('theme', '')}")
    if pkg.get("why"):
        st.markdown(f"""<div class="tip-card"><strong>为什么发这个：</strong>{pkg['why']}</div>""", unsafe_allow_html=True)
    if rec.get("reason"):
        st.markdown(f"""<div class="plan-card">📊 <strong>排期逻辑：</strong>{rec['reason']}</div>""", unsafe_allow_html=True)

    # 数据驱动排期说明
    if pkg.get("weekly_update_note"):
        st.markdown(f"""<div class="plan-card"><strong>🗓️ 本周自动更新：</strong>{pkg['weekly_update_note']}</div>""", unsafe_allow_html=True)

    if pkg.get("data_driven_note"):
        st.markdown(f"""<div class="tip-card" style="border-left-color:#4CAF50">{pkg['data_driven_note']}</div>""", unsafe_allow_html=True)

    latest_ops = get_latest_operations_snapshot()
    if latest_ops:
        metrics = latest_ops.get("metrics", {})
        period = latest_ops.get("period", {})
        sources = latest_ops.get("traffic_sources") or []
        source_parts = [f"{item.get('name', '')} {item.get('percent', 0)}%" for item in sources[:4]]
        time_info = latest_ops.get("viewer_time") or {}
        summary_parts = []
        if period.get("start") and period.get("end"):
            summary_parts.append(f"统计周期 {period['start']} 至 {period['end']}")
        if metrics.get("views"):
            summary_parts.append(f"观看总数 {int(metrics['views']):,}")
        if metrics.get("viewer_followers"):
            summary_parts.append(f"观看粉丝 {int(metrics['viewer_followers']):,}")
        if metrics.get("avg_watch_seconds"):
            summary_parts.append(f"平均观看时长 {int(metrics['avg_watch_seconds'])} 秒")
        if metrics.get("conversion_rate") is not None:
            summary_parts.append(f"转化率 {metrics.get('conversion_rate', 0)}%")
        if source_parts:
            summary_parts.append(f"来源结构 {' / '.join(source_parts)}")
        if time_info.get("peak_window"):
            peak_label = time_info["peak_window"]
            if time_info.get("peak_hour_label"):
                peak_label = f"{peak_label}（{time_info['peak_hour_label']}）"
            summary_parts.append(f"流量高峰 {peak_label}")

        st.markdown(
            f"""<div class="plan-card"><strong>📈 最新运营总结：</strong>{'；'.join(summary_parts)}。</div>""",
            unsafe_allow_html=True,
        )

    if pkg.get("tool_focus"):
        st.markdown("### 🛠️ 今日工具优先级")
        for t in pkg["tool_focus"]:
            name = t.get("name", "")
            reason = t.get("reason", "")
            action = t.get("action", "")
            st.markdown(f"**{name}**")
            st.markdown(f"- **原因：** {reason}")
            st.markdown(f"- **行动：** {action}")
            st.markdown("")

    if pkg.get("execution_focus"):
        st.markdown("### 📌 今日执行重点")
        for i, line in enumerate(pkg["execution_focus"], 1):
            st.markdown(f"{i}. {line}")

    if pkg.get("weekly_actions"):
        st.markdown("### 🗓️ 本周工具自动调整")
        for line in pkg["weekly_actions"][:4]:
            st.markdown(f"- {line}")

    st.markdown("---")

    # 季节性AI提示词建议
    if rec.get("season_prompt_tips"):
        with st.expander("🌿 当季AI创作色调建议（Prompt参考）", expanded=False):
            st.markdown(rec["season_prompt_tips"])

    # Prompt区域
    if pkg.get("prompts"):
        st.markdown("### 🎨 Step 1：复制Prompt去生成图片")
        for i, p in enumerate(pkg["prompts"], 1):
            with st.expander(f"🖼️ {p['desc']}", expanded=(i <= 2)):
                st.code(p["prompt"], language=None)
                if p.get("note"):
                    st.caption(f"💡 {p['note']}")

        st.markdown("---")

    # 封面
    if pkg.get("cover_text"):
        st.markdown("### 🖼️ Step 2：做封面")
        st.markdown(f"""<div class="plan-card">
            <strong>封面文字：</strong>{pkg['cover_text']}<br>
            <small>用Canva/醒图，画作占80% + 底部加粗体白字标题</small>
        </div>""", unsafe_allow_html=True)
        st.markdown("---")

    # 文案
    st.markdown("### ✍️ Step 3：复制文案发布")
    if pkg.get("title"):
        st.markdown("**标题（直接复制）：**")
        st.code(pkg["title"], language=None)

    if pkg.get("body"):
        st.markdown("**正文（直接复制）：**")
        st.text_area("正文内容", pkg["body"], height=400, key="daily_body", label_visibility="collapsed")

    if pkg.get("hashtags"):
        st.markdown("**标签（直接复制）：**")
        st.code(pkg["hashtags"], language=None)

    # 完整复制区
    if pkg.get("title") and pkg.get("body"):
        full = f"{pkg['title']}\n\n{pkg['body']}\n\n{pkg.get('hashtags', '')}"
        with st.expander("📋 一键复制完整文案"):
            st.text_area("完整文案", full, height=500, key="daily_full", label_visibility="collapsed")

    st.markdown("---")

    # 发布checklist
    st.markdown("### ✅ Step 4：发布前检查")
    checks = [
        f"⏰ 在 **{pkg.get('time', '21:00')}** 发布",
        "🖼️ 图片全部高清（≥1080px），没有水印",
        "📐 封面3:4竖版，文字在手机缩略图上能看清",
        "🏷️ 标签已全部添加（8-10个，与内容高度相关）",
        "🤖 **勾选「AI辅助创作」标签**（使用了MJ/SD/GPT等AI工具必须勾选！）",
        "📝 正文末尾有「⚠️ 本文图片由AI辅助生成」说明",
        "🚫 检查有无绝对化用语（最/第一/100%/必须等→改为「个人觉得」「亲测」）",
        "📍 发布后 **1小时内保持在线** 回复评论",
        "💬 发布后 **5分钟内** 自己在评论区留1条补充信息（≥15字）",
    ]
    for c in checks:
        st.markdown(f"- {c}")

    # 本周预览
    st.markdown("---")
    st.markdown("### 📅 本周内容预览")
    week = get_weekly_packages()
    for wpkg in week:
        today_mark = " ← **今天**" if wpkg.get("is_today") else ""
        holiday_mark = " 🔥" if wpkg.get("is_holiday") else ""
        st.markdown(
            f"- **{wpkg['weekday']}** {wpkg['date']}（{wpkg.get('time', '21:00')}）：{wpkg['type']}「{wpkg['theme']}」{today_mark}{holiday_mark}"
        )





def render_morning_patrol():
    st.markdown("""
    <div class="main-header">
        <h1>🌅 晨间工作台</h1>
        <p>每天10分钟 · 查数据 → 回评论 → 确认今日计划 → 开始干活</p>
    </div>
    """, unsafe_allow_html=True)

    account = get_account_info()
    followers = account.get("followers", 0) if account else 0
    today_pkg = get_today_package()
    today_eng = get_today_engagement()
    streak = get_engagement_streak()

    # 顶部快速概览
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <h3>{followers:,}</h3><p>👥 当前粉丝</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <h3>{streak}</h3><p>🔥 连续互动天数</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <h3>{today_eng.get('total_actions', 0)}</h3><p>💬 今日互动次数</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        health = calculate_account_health()
        st.markdown(f"""<div class="metric-card">
            <h3>{health.get('overall_score', 0)}</h3><p>🏥 健康度</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # 今日时间块计划
    st.markdown("### 📋 今日工作流程")
    for block_key, block in DAILY_TIME_BLOCKS.items():
        with st.expander(f"{block['label']}｜{block['time']}", expanded=(block_key in ("morning", "publish"))):
            for task in block["tasks"]:
                st.markdown(f"- {task}")

    st.markdown("---")

    # 今日内容计划速览
    st.markdown("### 🎯 今日发布计划")
    st.markdown(f"""<div class="plan-card">
        <strong>📌 内容类型：</strong>{today_pkg.get('type', '待安排')}<br>
        <strong>🎨 主题：</strong>{today_pkg.get('theme', '待确定')}<br>
        <strong>⏰ 推荐时间：</strong>{today_pkg.get('time', '21:00')}<br>
        <strong>📅 {today_pkg.get('date', '')} {today_pkg.get('weekday', '')}</strong>
    </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📌 去今日执行页面", use_container_width=True):
            go_to_page("📌 今日执行")
    with col_b:
        if st.button("✍️ 去生成内容", use_container_width=True):
            if ai_enabled():
                go_to_page("✍️ AI内容生成")
            else:
                go_to_page("⚙️ 设置")

    st.markdown("---")

    # 正在追踪的笔记
    active = get_active_tracking()
    if active:
        st.markdown("### ⏱️ 正在追踪的笔记")
        for t in active:
            publish_time = t.get("publish_time", "")
            if publish_time:
                pub_dt = datetime.datetime.fromisoformat(publish_time)
                hours_ago = (datetime.datetime.now() - pub_dt).total_seconds() / 3600
                next_checkpoint = "1h" if hours_ago < 1 else "24h" if hours_ago < 24 else "72h"
                st.markdown(f"""<div class="tip-card">
                    📊 「{t.get('title', '')}」发布于 {hours_ago:.0f} 小时前 →
                    下一个检查点：<strong>{POST_CHECKPOINTS[next_checkpoint]['label']}</strong>
                </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # 运营简报（纯模板引擎，不需要API Key，瞬间生成）
    st.markdown("### ☀️ 运营简报")
    if st.button("📋 生成今日运营简报", type="primary", use_container_width=True, key="gen_briefing"):
        posts = get_all_posts()
        yesterday_posts = posts[-3:] if posts else []
        briefing = generate_morning_briefing(
            yesterday_posts=yesterday_posts,
            account_info=account if account else {},
            today_plan=today_pkg,
            engagement_stats=today_eng,
            health_score=health.get("overall_score", 0),
        )
        st.markdown(briefing)


# ==================== 页面：发后跟踪器 ====================


