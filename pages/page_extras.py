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



def render_experience_vault():
    st.markdown("""
    <div class="main-header">
        <h1>📚 经验宝库</h1>
        <p>从你的历史数据中自动提炼规律 · 数据说了算 · 用经验指导下一步</p>
    </div>
    """, unsafe_allow_html=True)

    insights = extract_historical_insights()

    if not insights["has_data"]:
        st.info(f"📌 需要至少3篇有数据的笔记才能提炼经验。当前已有 {insights['total_posts']} 篇笔记，{insights['tracked_posts']} 篇有数据记录。")
        st.markdown("""
        <div class="tip-card">
            <strong>📝 怎么积累数据？</strong><br>
            1. 在「📝 笔记管理」中记录发布的笔记<br>
            2. 发布24h/72h后更新浏览/点赞/收藏/评论数据<br>
            3. 积累3篇以上有数据的笔记后，经验宝库就能自动分析规律了
        </div>
        """, unsafe_allow_html=True)
        return

    # ===== 顶部速览 =====
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        trend_emoji = "📈" if insights["performance_trend"] == "improving" else "📉" if insights["performance_trend"] == "declining" else "➡️"
        trend_label = "上升中" if insights["performance_trend"] == "improving" else "下降中" if insights["performance_trend"] == "declining" else "平稳"
        st.markdown(f"""<div class="metric-card">
            <h3>{trend_emoji}</h3><p>整体趋势·{trend_label}</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <h3>{insights.get('best_content_type', '—')}</h3><p>🏆 最佳内容类型</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <h3>{insights.get('best_posting_time', '—')}</h3><p>⏰ 最佳发布时间</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <h3>{insights.get('best_posting_day', '—')}</h3><p>📅 最佳发布日</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    tab_patterns, tab_ranking, tab_benchmarks, tab_mix = st.tabs([
        "💡 发现的规律",
        "📊 内容类型排名",
        "📈 动态基准线",
        "🎯 配比建议",
    ])

    # ===== Tab 1: 发现的规律 =====
    with tab_patterns:
        st.markdown("### 💡 AI从你的数据中发现的规律")

        if insights["discovered_patterns"]:
            for pattern in insights["discovered_patterns"]:
                st.markdown(f"""<div class="tip-card">{pattern}</div>""", unsafe_allow_html=True)
        else:
            st.info("数据量还不够，继续发布笔记并记录数据，规律会自动浮现")

        st.markdown("---")

        # 最佳 vs 最差笔记对比
        top_posts = insights.get("top_posts", [])
        bottom_posts = insights.get("bottom_posts", [])

        if top_posts or bottom_posts:
            st.markdown("### 🏆 vs ❌ 最佳 vs 最差笔记对比")
            st.markdown("_对比你的「爆款」和「哑火」笔记，找出差异_")

            col_good, col_bad = st.columns(2)
            with col_good:
                st.markdown("**🏆 表现最好**")
                for p in top_posts:
                    m = p.get("latest_metrics", {})
                    st.markdown(f"""<div class="plan-card" style="border-left:4px solid #4CAF50">
                        <strong>「{p.get('title', '')}」</strong><br>
                        <small>{p.get('content_type', '')}｜{p.get('post_date', '')} {p.get('post_time', '')}</small><br>
                        👀{m.get('views', 0)} ❤️{m.get('likes', 0)} ⭐{m.get('saves', 0)} 💬{m.get('comments', 0)}
                    </div>""", unsafe_allow_html=True)

            with col_bad:
                st.markdown("**❌ 表现最差**")
                for p in bottom_posts:
                    m = p.get("latest_metrics", {})
                    st.markdown(f"""<div class="plan-card" style="border-left:4px solid #f44336">
                        <strong>「{p.get('title', '')}」</strong><br>
                        <small>{p.get('content_type', '')}｜{p.get('post_date', '')} {p.get('post_time', '')}</small><br>
                        👀{m.get('views', 0)} ❤️{m.get('likes', 0)} ⭐{m.get('saves', 0)} 💬{m.get('comments', 0)}
                    </div>""", unsafe_allow_html=True)

            st.markdown("""<div class="tip-card">
                <strong>💡 对比方法：</strong>看看最好和最差的笔记，在<strong>标题结构、内容类型、发布时间、封面风格</strong>上有什么区别？
                差异就是你的「爆款密码」。
            </div>""", unsafe_allow_html=True)

    # ===== Tab 2: 内容类型排名 =====
    with tab_ranking:
        st.markdown("### 📊 内容类型表现排名")
        st.markdown("_按平均浏览量排序，数据说了算_")

        ranking = insights.get("content_type_ranking", [])
        if ranking:
            # 柱状图
            df_rank = pd.DataFrame(ranking)
            if len(df_rank) > 0:
                fig = px.bar(
                    df_rank, x="type", y=["avg_views", "avg_likes", "avg_saves"],
                    barmode="group",
                    labels={"type": "内容类型", "value": "数量", "variable": "指标"},
                    color_discrete_sequence=["#533483", "#0f3460", "#e94560"],
                )
                fig.update_layout(height=400, template="plotly_white",
                                  margin=dict(l=20, r=20, t=20, b=40))
                st.plotly_chart(fig, use_container_width=True)

            # 排名列表
            for i, ct in enumerate(ranking, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
                st.markdown(f"""<div class="plan-card">
                    <strong>{medal} {ct['type']}</strong>（{ct['count']}篇）<br>
                    平均浏览 <strong>{ct['avg_views']}</strong> · 平均点赞 {ct['avg_likes']} · 平均收藏 {ct['avg_saves']} · 收藏率 {ct['save_rate']}%
                </div>""", unsafe_allow_html=True)

        # 时间排名
        time_ranking = insights.get("time_ranking", [])
        if time_ranking:
            st.markdown("### ⏰ 发布时间表现排名")
            for t in time_ranking:
                st.markdown(f"- **{t['hour']}:00** 发布（{t['count']}篇）→ 平均浏览 **{t['avg_views']}**")

        # 星期排名
        day_ranking = insights.get("day_ranking", [])
        if day_ranking:
            st.markdown("### 📅 发布星期表现排名")
            for d in day_ranking:
                st.markdown(f"- **{d['day']}** 发布（{d['count']}篇）→ 平均浏览 **{d['avg_views']}**")

    # ===== Tab 3: 动态基准线 =====
    with tab_benchmarks:
        st.markdown("### 📈 基于自身数据的动态基准线")
        st.markdown("_不和别人比，和自己的历史最好成绩比_")

        benchmarks = get_dynamic_benchmarks()
        if benchmarks.get("has_data"):
            st.markdown(f"_基于 **{benchmarks['total_posts']}** 篇有数据的笔记计算_")

            for metric, labels in [
                ("views", ("👀 浏览量", "")),
                ("likes", ("❤️ 点赞数", "")),
                ("saves", ("⭐ 收藏数", "")),
                ("comments", ("💬 评论数", "")),
            ]:
                b = benchmarks["benchmarks"][metric]
                st.markdown(f"""<div class="plan-card">
                    <strong>{labels[0]}</strong><br>
                    📊 历史均值：<strong>{b['avg']}</strong>（及格线）
                    ｜🏆 Top30%均值：<strong>{b['top30']}</strong>（优秀线）
                    ｜👑 历史最高：<strong>{b['best']}</strong>
                </div>""", unsafe_allow_html=True)

            st.markdown("""<div class="tip-card">
                <strong>💡 用法：</strong>发布新笔记后，对比动态基准线。<br>
                超过「Top30%均值」= 优秀！低于「历史均值」= 需要复盘原因。<br>
                随着你的笔记越来越好，基准线会自动提升。
            </div>""", unsafe_allow_html=True)
        else:
            st.info(benchmarks.get("message", "数据不足"))

    # ===== Tab 4: 配比建议 =====
    with tab_mix:
        st.markdown("### 🎯 数据驱动的内容配比建议")
        st.markdown("_基于你的历史数据表现，推荐的最优内容配比_")

        mix = insights.get("content_mix_suggestion", [])
        if mix:
            # 饼图
            labels = [m["type"] for m in mix]
            values = [m["percentage"] for m in mix]
            fig_pie = px.pie(
                names=labels, values=values,
                color_discrete_sequence=px.colors.sequential.Purples_r,
            )
            fig_pie.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_pie, use_container_width=True)

            for m in mix:
                role_color = "#4CAF50" if "主力" in m["role"] else "#FF9800" if "辅助" in m["role"] else "#9E9E9E"
                st.markdown(f"""<div class="plan-card" style="border-left:4px solid {role_color}">
                    <strong>{m['type']}</strong> → 建议占比 <strong>{m['percentage']}%</strong>（{m['role']}）<br>
                    <small>📊 {m['reason']}</small>
                </div>""", unsafe_allow_html=True)

            st.markdown("""<div class="tip-card">
                <strong>📌 应用方法：</strong>每周发5篇的话，按上面的配比安排内容类型。<br>
                每2周重新来看这个页面，配比会随着新数据自动调整。
            </div>""", unsafe_allow_html=True)
        else:
            st.info("发布更多不同类型的内容后，这里会自动生成最优配比建议")


# ==================== 页面：热点快反 ====================



def render_hot_topic():
    st.markdown("""
    <div class="main-header">
        <h1>⚡ 热点快反</h1>
        <p>看到热点 → 30秒描述 → AI一键生成完整内容包 → 直接发布</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tip-card">
        <strong>💡 什么时候用这个功能？</strong><br>
        • 看到艺术圈大新闻（画家去世/天价拍卖/大展开幕）<br>
        • 看到社会热点可以和艺术结合（节日/影视/事件）<br>
        • 发现小红书上某个话题突然火了<br>
        • 想蹭热点但不知道怎么和自己的账号结合
    </div>
    """, unsafe_allow_html=True)

    tab_quick, tab_recent = st.tabs(["⚡ 快速出内容", "📅 近期热点日历"])

    with tab_quick:
        st.markdown("### ⚡ 描述热点 → 一键生成内容包")

        hot_desc = st.text_area("🔥 热点描述",
                                 height=120,
                                 placeholder="描述你看到的热点，例如：\n"
                                 "• 「今天Gerhard Richter的一幅画在苏富比拍出了3000万美元」\n"
                                 "• 「春天来了，小红书上樱花主题很火」\n"
                                 "• 「某个AI绘画工具发布了新版本」\n"
                                 "• 「某个电影里出现了一幅名画，引发讨论」",
                                 key="hot_desc")

        col1, col2 = st.columns(2)
        with col1:
            hot_urgency = st.selectbox("⏰ 紧急程度", [
                "🔴 今天必须发（时效性极强）",
                "🟡 明天之前发（有一定时效）",
                "🟢 本周内发（不太紧急）",
            ], key="hot_urgency")
        with col2:
            hot_angle = st.text_input("🎯 你想从什么角度切入（可选）",
                                       placeholder="例如：用AI模仿他的风格 / 做一个合集 / 讲一个故事",
                                       key="hot_angle")

        if hot_angle:
            hot_desc_full = f"{hot_desc}\n\n我想从这个角度切入：{hot_angle}"
        else:
            hot_desc_full = hot_desc

        if st.button("⚡ 一键生成完整内容包", type="primary", use_container_width=True, key="gen_hot_btn"):
            if not hot_desc:
                st.warning("请描述热点内容")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                urgency_text = hot_urgency.split("（")[0].replace("🔴 ", "").replace("🟡 ", "").replace("🟢 ", "")
                with st.spinner("🤖 AI正在生成完整内容包..."):
                    result = generate_hot_topic_package(hot_desc_full, urgency_text)
                st.success("✅ 内容包生成完成！按步骤执行即可")
                st.markdown(result)

        # 快捷热点入口
        st.markdown("---")
        st.markdown("### 🎯 常见可蹭热点（一键快填）")
        quick_topics = [
            ("🎨 画家大事件", "有一位知名画家最近发生了大事（去世/获奖/大展开幕/创纪录拍卖），需要快速出一篇"),
            ("💰 天价拍卖", "最近有一幅油画在拍卖场上创下了高价记录"),
            ("🤖 AI工具更新", "某个AI绘画工具（MJ/SD/DALL-E）发布了重大更新或新功能"),
            ("📅 节日蹭热", "即将到来的节日想做一篇和艺术结合的内容"),
            ("🎬 影视联名", "某部热门电影/电视剧/综艺出现了艺术相关的内容"),
        ]
        cols = st.columns(len(quick_topics))
        for i, (label, desc) in enumerate(quick_topics):
            with cols[i]:
                if st.button(label, key=f"quick_hot_{i}", use_container_width=True):
                    st.session_state["hot_desc"] = desc

    with tab_recent:
        st.markdown("### 📅 近7天热点日历")
        from xhs_agent.calendar_engine import get_nearby_events, get_current_season

        events = get_nearby_events(14)
        season = get_current_season()

        st.markdown(f"""<div class="plan-card">
            🌿 当前季节：<strong>{season['name']}</strong><br>
            🎨 推荐色调：{season['colors']}<br>
            📌 推荐主题：{season['subjects']}
        </div>""", unsafe_allow_html=True)

        if events:
            for event in events:
                heat_bar = event.get("heat", "★")
                days = event.get("days_away", 0)
                urgency = "🔴 今天！" if days == 0 else f"📅 还有{days}天" if days <= 3 else f"🗓️ {days}天后"
                st.markdown(f"""<div class="tip-card">
                    <strong>{urgency} · {event['date']} · {event['name']}</strong>（热度{heat_bar}）<br>
                    🎨 艺术角度：{event.get('art_angle', '')}<br>
                    📌 推荐选题：{event.get('topic', '')}
                </div>""", unsafe_allow_html=True)

                if days <= 1:
                    if st.button(f"⚡ 立即为「{event['name']}」生成内容",
                                  key=f"hot_event_{event['name']}", use_container_width=True):
                        st.session_state["hot_desc"] = f"今天是{event['name']}，想从「{event.get('art_angle', '')}」角度出一篇和{ACCOUNT_NICHE}结合的笔记"
                        st.info("请切换到「⚡ 快速出内容」Tab，热点描述已自动填入")
        else:
            st.info("未来14天没有预设的热点节日。但你可以自己发现热点并在「⚡ 快速出内容」中使用！")


# ==================== 页面：设置 ====================



def render_analytics():
    st.markdown("## 📊 数据分析")

    stats = get_overall_stats()

    if stats["total_posts"] == 0:
        st.info("📌 暂无数据。请先在「笔记管理」页面添加笔记和数据记录。")

        st.markdown("### 📈 艺术账号数据追踪指南")
        st.markdown("""
        为了获得精准的运营分析，建议你：
        1. **发布笔记后**：在「笔记管理」中记录笔记信息
        2. **发布24小时后**：记录第一次数据（浏览/点赞/收藏/评论）
        3. **发布72小时后**：再次更新数据
        4. **每周日**：查看本周整体数据分析

        > 💡 艺术类内容的特点：收藏率通常高于普通内容（因为有审美价值），但初始流量可能较低。
        > 优质的画家介绍和AI教程类内容有很强的「长尾流量」，发布后1-4周仍可能持续获得搜索流量。
        """)
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总浏览量", f"{stats.get('total_views', 0):,}")
    with col2:
        st.metric("总点赞数", f"{stats.get('total_likes', 0):,}")
    with col3:
        st.metric("总收藏数", f"{stats.get('total_saves', 0):,}")
    with col4:
        st.metric("总评论数", f"{stats.get('total_comments', 0):,}")

    st.markdown("---")

    trend = get_trend_data()
    if trend:
        st.markdown("### 📈 数据趋势")
        df_trend = pd.DataFrame(trend)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_trend["date"], y=df_trend["views"],
                                 mode="lines+markers", name="浏览量",
                                 line=dict(color="#533483", width=2)))
        fig.add_trace(go.Scatter(x=df_trend["date"], y=df_trend["likes"],
                                 mode="lines+markers", name="点赞",
                                 line=dict(color="#0f3460", width=2)))
        fig.add_trace(go.Scatter(x=df_trend["date"], y=df_trend["saves"],
                                 mode="lines+markers", name="收藏",
                                 line=dict(color="#e94560", width=2)))
        fig.update_layout(
            height=400, template="plotly_white",
            legend=dict(orientation="h", y=-0.15),
            margin=dict(l=20, r=20, t=20, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    type_stats = get_content_type_analysis()
    if type_stats:
        st.markdown("### 📊 内容类型表现对比")
        st.markdown("_哪类内容表现最好？画家赏析 vs AI创作 vs 教程？_")
        df_type = pd.DataFrame([
            {"类型": k, "平均浏览": v["avg_views"], "平均点赞": v["avg_likes"],
             "平均收藏": v["avg_saves"], "笔记数": v["count"]}
            for k, v in type_stats.items()
        ])
        fig2 = px.bar(df_type, x="类型", y=["平均浏览", "平均点赞", "平均收藏"],
                       barmode="group", color_discrete_sequence=["#533483", "#0f3460", "#e94560"])
        fig2.update_layout(height=350, template="plotly_white",
                           margin=dict(l=20, r=20, t=20, b=40))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 💡 数据优化建议")
    avg_metrics = {
        "views": stats["avg_views"],
        "likes": stats["avg_likes"],
        "saves": stats["avg_saves"],
        "comments": stats["avg_comments"],
        "shares": stats.get("avg_shares", 0),
    }
    tips = get_optimization_tips(avg_metrics)
    for tip in tips:
        if isinstance(tip, dict):
            status_emoji = "🟢" if tip["status"] == "优秀" else "🟡" if tip["status"] == "一般" else "🔴"
            st.markdown(f"""
            <div class="tip-card">
                <strong>{status_emoji} {tip['metric']}: {tip['value']} ({tip['status']})</strong>
            </div>
            """, unsafe_allow_html=True)
            for advice in tip["advice"]:
                st.markdown(f"  - {advice}")
        else:
            st.info(tip)


# ==================== 页面：涨粉策略 ====================


