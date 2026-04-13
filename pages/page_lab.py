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



def render_viral_lab():
    st.markdown("""
    <div class="main-header">
        <h1>🔥 爆款实验室</h1>
        <p>拆解爆款基因 · 发布前检测 · 内容二创 · AI周报</p>
    </div>
    """, unsafe_allow_html=True)

    tab_analyze, tab_precheck, tab_repurpose, tab_report = st.tabs([
        "🔍 爆款拆解器",
        "🧪 发布前检测",
        "🔄 内容二创",
        "📋 AI周报",
    ])

    # ==================== Tab 1: 爆款拆解器 ====================
    with tab_analyze:
        st.markdown("### 🔍 爆款拆解器")
        st.markdown("""
        <div class="tip-card">
            <strong>用法：</strong>在小红书上看到一篇数据很好的笔记（不限领域），把标题和内容粘贴进来。
            AI帮你深度拆解为什么火，并提取可复用到你的艺术账号的模板。
        </div>
        """, unsafe_allow_html=True)

        v_title = st.text_input("📌 爆款笔记标题", placeholder="粘贴笔记标题", key="v_title")
        v_content = st.text_area("📝 爆款笔记内容", height=200,
                                  placeholder="粘贴笔记正文内容...\n（不用很完整，关键段落即可）",
                                  key="v_content")
        v_metrics = st.text_input("📊 数据表现（可选）",
                                   placeholder="例如：浏览10万，点赞5000，收藏8000，评论500",
                                   key="v_metrics")

        if st.button("🔍 开始拆解", type="primary", use_container_width=True, key="analyze_viral_btn"):
            if not v_title and not v_content:
                st.warning("请至少输入标题或内容")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner("🤖 正在深度拆解爆款基因..."):
                    result = analyze_viral_post(v_title, v_content, v_metrics)
                st.success("✅ 拆解完成！")
                st.markdown(result)

    # ==================== Tab 2: 发布前检测 ====================
    with tab_precheck:
        st.markdown("### 🧪 发布前爆款潜力检测")
        st.markdown("""
        <div class="tip-card">
            <strong>用法：</strong>在发布笔记之前，把你的标题和内容粘贴进来。
            AI会从5个维度评分，告诉你哪里需要改、怎么改，确保每篇都达到最佳状态。
        </div>
        """, unsafe_allow_html=True)

        p_title = st.text_input("📌 你的笔记标题", placeholder="输入你准备发布的标题", key="pc_title")
        p_content = st.text_area("📝 你的笔记正文", height=250,
                                  placeholder="粘贴你的笔记正文...",
                                  key="pc_content")

        col1, col2 = st.columns(2)
        with col1:
            p_cover = st.text_input("🖼️ 封面描述（可选）",
                                     placeholder="简单描述你的封面图是什么样的",
                                     key="pc_cover")
        with col2:
            p_time = st.text_input("⏰ 计划发布时间（可选）",
                                    placeholder="例如：今晚21:00 / 周六上午10:00",
                                    key="pc_time")

        # 展示评分维度参考
        with st.expander("📊 评分维度说明"):
            for dim_name, dim_info in VIRAL_SCORE_DIMENSIONS.items():
                st.markdown(f"**{dim_name}**（权重{dim_info['weight']}%）")
                for c in dim_info["criteria"]:
                    st.markdown(f"  - {c}")

        if st.button("🧪 开始检测", type="primary", use_container_width=True, key="precheck_btn"):
            if not p_title and not p_content:
                st.warning("请至少输入标题或内容")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner("🤖 正在全方位评估你的内容..."):
                    result = pre_publish_check(p_title, p_content, p_cover, p_time)
                st.success("✅ 检测完成！")
                st.markdown(result)

    # ==================== Tab 3: 内容二创 ====================
    with tab_repurpose:
        st.markdown("### 🔄 内容二创工具")
        st.markdown("""
        <div class="tip-card">
            <strong>同一份内容素材，换个形式就是新内容。</strong>
            一篇好的图文笔记可以变成：短视频脚本、合集笔记、系列连载、英文版、速查清单。
            工作量增加30%，但内容产出翻5倍。
        </div>
        """, unsafe_allow_html=True)

        r_title = st.text_input("📌 原内容标题", placeholder="输入要二创的笔记标题", key="rp_title")
        r_content = st.text_area("📝 原内容正文", height=200,
                                  placeholder="粘贴原笔记正文...",
                                  key="rp_content")

        st.markdown("**🎯 选择二创方向：**")
        repurpose_cols = st.columns(len(CONTENT_REPURPOSE_MAP))
        selected_format = None
        for i, (fmt_name, fmt_info) in enumerate(CONTENT_REPURPOSE_MAP.items()):
            with repurpose_cols[i]:
                st.markdown(f"""<div class="plan-card" style="min-height:120px">
                    <strong>{fmt_name}</strong><br>
                    <small>{fmt_info['desc']}</small><br>
                    <small style="color:#533483">💡 {fmt_info['tips']}</small>
                </div>""", unsafe_allow_html=True)
                if st.button(f"选择", key=f"rp_fmt_{i}", use_container_width=True):
                    selected_format = fmt_name

        if selected_format:
            st.session_state["rp_selected_format"] = selected_format

        current_format = st.session_state.get("rp_selected_format")
        if current_format:
            st.info(f"已选择：**{current_format}**")

        if st.button("🔄 开始二创", type="primary", use_container_width=True, key="repurpose_btn"):
            fmt = st.session_state.get("rp_selected_format")
            if not r_title and not r_content:
                st.warning("请输入原内容")
            elif not fmt:
                st.warning("请选择一个二创方向")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner(f"🤖 正在将内容改编为「{fmt}」..."):
                    result = repurpose_content(r_title, r_content, fmt)
                st.success(f"✅ {fmt} 二创完成！")
                st.markdown(result)

    # ==================== Tab 4: AI周报 ====================
    with tab_report:
        st.markdown("### 📋 AI智能周报")
        st.markdown("""
        <div class="tip-card">
            <strong>每周日点一下，AI自动分析本周所有笔记数据，</strong>
            总结表现、发现问题、给出下周计划。比你自己分析快100倍。
        </div>
        """, unsafe_allow_html=True)

        account = get_account_info()
        posts = get_all_posts()

        # 本周数据快照
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📝 总笔记数", len(posts))
        with col2:
            st.metric("👥 当前粉丝", account.get("followers", 0) if account else 0)

        if st.button("📋 生成本周AI周报", type="primary", use_container_width=True, key="gen_report_btn"):
            if not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            elif not posts:
                st.warning("暂无笔记数据。请先在「笔记管理」中记录笔记后再生成周报。")
            else:
                with st.spinner("🤖 正在分析数据并生成周报..."):
                    # 保存周快照
                    save_weekly_snapshot()
                    report = generate_weekly_report(posts, account if account else {})
                st.success("✅ 周报生成完成！")
                st.markdown(report)

        # 历史快照
        snapshots = get_weekly_snapshots()
        if snapshots:
            with st.expander("📊 历史周数据快照"):
                for snap in reversed(snapshots[-10:]):
                    week = snap.get("week", "未知")
                    st.markdown(f"""<div class="plan-card">
                        <strong>📅 {week}</strong>（{snap.get('date', '')[:10]}）<br>
                        笔记 {snap.get('total_posts', 0)} 篇 · 平均浏览 {snap.get('avg_views', 0)} · 平均点赞 {snap.get('avg_likes', 0)} · 平均收藏 {snap.get('avg_saves', 0)}
                    </div>""", unsafe_allow_html=True)


# ==================== 页面：评论引流 ====================



def render_account_health():
    st.markdown("""
    <div class="main-header">
        <h1>🏥 账号体检</h1>
        <p>5大维度全方位诊断 · AI开处方 · 30天改善计划</p>
    </div>
    """, unsafe_allow_html=True)

    health = calculate_account_health()
    account = get_account_info()
    stats = get_overall_stats()
    posts = get_all_posts()

    # 总分大卡片
    score = health.get("overall_score", 0)
    level = health.get("level", "待评估")
    score_color = "#4CAF50" if score >= 80 else "#FF9800" if score >= 60 else "#f44336" if score >= 40 else "#9E9E9E"

    st.markdown(f"""
    <div style="text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(10,22,40,0.95) 0%, rgba(6,13,20,0.98) 100%); border-radius:16px; border:2px solid {score_color}; margin-bottom:1.5rem; box-shadow:0 0 24px rgba(0,0,0,0.25);">
        <h1 style="font-size:4rem; color:{score_color}; margin:0;">{score}</h1>
        <p style="font-size:1.5rem; color:#e2e8f0; margin:0.5rem 0;">{level}</p>
        <p style="color:#8fa3bb; font-size:0.9rem;">账号综合健康度</p>
    </div>
    """, unsafe_allow_html=True)

    if health.get("summary"):
        st.info(health["summary"])
        return

    # 各维度得分
    st.markdown("### 📊 各维度体检结果")
    dimensions = health.get("dimensions", {})

    dim_cols = st.columns(len(dimensions))
    for i, (dim_name, dim_info) in enumerate(dimensions.items()):
        with dim_cols[i]:
            dim_score = dim_info.get("score", 0)
            dim_level = dim_info.get("level", "未知")
            dim_color = "#4CAF50" if dim_score >= 80 else "#FF9800" if dim_score >= 60 else "#f44336" if dim_score >= 40 else "#9E9E9E"
            st.markdown(f"""<div class="metric-card" style="border-left:4px solid {dim_color}">
                <h3 style="color:{dim_color}">{dim_score}</h3>
                <p style="font-weight:bold">{dim_name}</p>
                <p style="font-size:0.8rem">{dim_level}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # 各维度详情
    for dim_name, dim_info in dimensions.items():
        dim_config = ACCOUNT_HEALTH_DIMENSIONS.get(dim_name, {})
        dim_score = dim_info.get("score", 0)
        icon = "🟢" if dim_score >= 80 else "🟡" if dim_score >= 60 else "🟠" if dim_score >= 40 else "🔴"
        with st.expander(f"{icon} {dim_name}：{dim_score}分（权重{dim_info.get('weight', 0)}%）"):
            st.markdown(f"**评估内容：** {dim_info.get('description', '')}")
            st.markdown(f"**✅ 优秀标准：** {dim_config.get('good', '')}")
            st.markdown(f"**❌ 需改善：** {dim_config.get('bad', '')}")

    st.markdown("---")

    # 雷达图
    if dimensions:
        categories = list(dimensions.keys())
        values = [dimensions[c]["score"] for c in categories]
        values.append(values[0])  # 闭合
        categories.append(categories[0])

        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line=dict(color="#533483"),
            fillcolor="rgba(83,52,131,0.15)",
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=400,
            margin=dict(l=60, r=60, t=40, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # AI诊断报告
    st.markdown("### 🤖 AI深度诊断")
    if st.button("🏥 生成AI诊断报告", type="primary", use_container_width=True, key="gen_diagnosis"):
        if not OPENAI_API_KEY:
            st.error(AI_SETUP_ERROR)
        else:
            with st.spinner("🤖 正在全面诊断..."):
                report = generate_account_diagnosis(
                    health_data=health,
                    stats=stats,
                    posts=posts,
                    account_info=account if account else {},
                )
            st.markdown(report)


# ==================== 页面：后链路分析 ====================



def render_funnel_analysis():
    st.markdown("""
    <div class="main-header">
        <h1>📈 后链路分析</h1>
        <p>曝光→点击→互动→主页→关注→私域→变现 · 每一步都有对应动作</p>
    </div>
    """, unsafe_allow_html=True)

    account = get_account_info()
    followers = account.get("followers", 0) if account else 0
    stage_name = "冷启动期" if followers < 1000 else "成长期" if followers < 10000 else "爆发期" if followers < 100000 else "稳定期"
    stage_focus = FUNNEL_HEALTH_BENCHMARKS.get(stage_name, {})

    # 阶段提示
    st.markdown(f"""<div class="tip-card">
        <strong>📍 你当前在「{stage_name}」，重点关注的后链路环节：</strong>
        {'、'.join(stage_focus.get('重点关注', []))}<br>
        <small>{stage_focus.get('说明', '')}</small>
    </div>""", unsafe_allow_html=True)

    tab_input, tab_result, tab_trend, tab_guide = st.tabs([
        "📊 录入数据",
        "🔍 漏斗诊断",
        "📈 趋势对比",
        "📖 后链路指南",
    ])

    # ===== Tab 1: 录入数据 =====
    with tab_input:
        st.markdown("### 📊 录入后链路数据")
        st.markdown("""
        <div class="tip-card">
            <strong>📌 数据来源：</strong>打开小红书创作者中心 → 数据概览/笔记分析 → 复制以下数据<br>
            <strong>📌 录入频率：</strong>建议每周录入一次整体数据，或者每篇重点笔记单独录入
        </div>
        """, unsafe_allow_html=True)

        scope = st.radio("📋 数据范围", ["📊 本周整体数据", "📝 单篇笔记数据"], horizontal=True, key="funnel_scope")

        if scope == "📝 单篇笔记数据":
            fn_title = st.text_input("📌 笔记标题", key="fn_title", placeholder="填写笔记标题")
            fn_type = st.selectbox("📋 内容类型", list(CONTENT_TYPES.keys()), key="fn_type")
        else:
            fn_title = f"整体数据·{datetime.datetime.now().strftime('%m月%d日')}"
            fn_type = "整体"

        st.markdown("#### 📢 曝光与点击（创作者中心 → 数据概览）")
        col1, col2 = st.columns(2)
        with col1:
            fn_impressions = st.number_input("📢 笔记曝光量", min_value=0, value=0, key="fn_impr",
                                              help="笔记在信息流/搜索中被展示的次数")
        with col2:
            fn_views = st.number_input("👀 浏览量（阅读量）", min_value=0, value=0, key="fn_views",
                                        help="点击进入笔记的人数")

        st.markdown("#### ❤️ 互动数据（创作者中心 → 互动分析）")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            fn_likes = st.number_input("❤️ 点赞", min_value=0, value=0, key="fn_likes")
        with col2:
            fn_saves = st.number_input("⭐ 收藏", min_value=0, value=0, key="fn_saves")
        with col3:
            fn_comments = st.number_input("💬 评论", min_value=0, value=0, key="fn_comments")
        with col4:
            fn_shares = st.number_input("🔄 分享", min_value=0, value=0, key="fn_shares")

        st.markdown("#### 🏠 转化数据（创作者中心 → 粉丝分析/流量分析）")
        col1, col2, col3 = st.columns(3)
        with col1:
            fn_profile = st.number_input("🏠 主页访问数", min_value=0, value=0, key="fn_profile",
                                          help="通过此笔记/本周访问你主页的人数")
        with col2:
            fn_follows = st.number_input("➕ 新增关注", min_value=0, value=0, key="fn_follows",
                                          help="通过此笔记/本周新增的粉丝数")
        with col3:
            fn_dms = st.number_input("📩 收到私信数", min_value=0, value=0, key="fn_dms",
                                      help="通过此笔记/本周收到的私信数")

        st.markdown("#### 📱 私域与变现（如有）")
        col1, col2, col3 = st.columns(3)
        with col1:
            fn_private = st.number_input("📱 私域新增人数", min_value=0, value=0, key="fn_private",
                                          help="新进微信群/知识星球/社群的人数")
        with col2:
            fn_paying = st.number_input("💰 付费人数", min_value=0, value=0, key="fn_paying",
                                         help="购买课程/产品/服务的人数")
        with col3:
            fn_revenue = st.number_input("💰 收入金额（元）", min_value=0, value=0, key="fn_revenue",
                                          help="本周/本篇带来的收入")

        if st.button("📊 提交并分析后链路", type="primary", use_container_width=True, key="submit_funnel"):
            if fn_views == 0 and fn_impressions == 0:
                st.warning("请至少填写曝光量或浏览量")
            else:
                record = {
                    "scope": "post" if scope == "📝 单篇笔记数据" else "weekly",
                    "title": fn_title,
                    "content_type": fn_type,
                    "impressions": fn_impressions,
                    "views": fn_views,
                    "likes": fn_likes,
                    "saves": fn_saves,
                    "comments": fn_comments,
                    "shares": fn_shares,
                    "profile_visits": fn_profile,
                    "new_followers": fn_follows,
                    "dms": fn_dms,
                    "private_domain_adds": fn_private,
                    "paying_customers": fn_paying,
                    "revenue": fn_revenue,
                }
                record_id = save_funnel_record(record)
                st.success(f"✅ 数据已保存！记录#{record_id}")

                # 算法加权评分
                algo = calculate_algorithm_score(record)
                pool = analyze_traffic_pool(record)

                col_algo, col_pool = st.columns(2)
                with col_algo:
                    st.markdown(f"""<div style="text-align:center; padding:1rem; background:#f8f5ff; border-radius:12px; border:2px solid #533483;">
                        <h3 style="color:#533483; margin:0;">算法评分 {algo['raw_score']}</h3>
                        <p style="color:#888; margin:0; font-size:0.85rem;">关注×8 + 评论×4 + 转发×4 + 点赞×1 + 收藏×1</p>
                    </div>""", unsafe_allow_html=True)
                with col_pool:
                    pool_info = pool["current_pool"]
                    pool_icon = "🟢" if pool["can_breakthrough"] else "🔴"
                    st.markdown(f"""<div style="text-align:center; padding:1rem; background:#f8f5ff; border-radius:12px; border:2px solid {'#4CAF50' if pool['can_breakthrough'] else '#f44336'};">
                        <h3 style="color:{'#4CAF50' if pool['can_breakthrough'] else '#f44336'}; margin:0;">{pool_icon} Level {pool_info['level']}</h3>
                        <p style="color:#888; margin:0; font-size:0.85rem;">流量池：曝光{pool_info['exposure']}</p>
                    </div>""", unsafe_allow_html=True)

                # 流量池突破检测
                if not pool["can_breakthrough"] and pool["breakthrough_actions"]:
                    st.markdown("### 🚀 流量池突破建议")
                    for action in pool["breakthrough_actions"][:4]:
                        st.markdown(f"""<div class="tip-card">{action}</div>""", unsafe_allow_html=True)

                # 算法提分建议
                if algo["optimization_priority"]:
                    st.markdown("### 📊 算法提分建议")
                    for opt in algo["optimization_priority"]:
                        st.markdown(f"- 📈 **{opt['metric']}**：{opt['reason']} → {opt['action']}")

                st.markdown("---")

                # 漏斗转化率分析
                funnel_results = calculate_funnel_rates(record)
                bottleneck = find_funnel_bottleneck(funnel_results)

                if funnel_results:
                    st.markdown("### 📊 漏斗转化率分析")
                    _render_funnel_results(funnel_results, bottleneck)

    # ===== Tab 2: 漏斗诊断 =====
    with tab_result:
        records = get_all_funnel_records()
        if not records:
            st.info("暂无后链路数据。请先在「📊 录入数据」Tab录入创作者中心的数据。")
        else:
            latest = records[-1]
            st.markdown(f"### 📊 最新数据：{latest.get('title', '')}（{latest.get('date', '')}）")

            funnel_results = calculate_funnel_rates(latest)
            bottleneck = find_funnel_bottleneck(funnel_results)
            comparison = get_funnel_comparison()

            if funnel_results:
                _render_funnel_results(funnel_results, bottleneck)

                # 对比变化
                if comparison.get("has_comparison"):
                    st.markdown("---")
                    st.markdown("### 📈 对比上次变化")
                    for c in comparison.get("changes", []):
                        delta_color = "green" if c["delta"] > 0 else "red" if c["delta"] < 0 else "gray"
                        st.markdown(f"""<div class="plan-card">
                            {c['name']}：<strong>{c['previous_rate']}%</strong> → <strong>{c['current_rate']}%</strong>
                            <span style="color:{delta_color}; font-weight:bold">（{c['direction']} {c['delta']:+.2f}%）</span>
                            {c['current_level']}
                        </div>""", unsafe_allow_html=True)

                # AI深度诊断
                st.markdown("---")
                if st.button("🤖 AI深度诊断后链路", type="primary", use_container_width=True, key="ai_funnel"):
                    if not OPENAI_API_KEY:
                        st.error(AI_SETUP_ERROR)
                    else:
                        with st.spinner("🤖 AI正在深度分析后链路漏斗..."):
                            report = generate_funnel_diagnosis(
                                funnel_results=funnel_results,
                                bottleneck=bottleneck,
                                account_info=account if account else {},
                                comparison=comparison,
                            )
                        st.markdown(report)

    # ===== Tab 3: 趋势对比 =====
    with tab_trend:
        trend = get_funnel_trend(20)
        if not trend:
            st.info("暂无历史数据。录入2次以上数据后可查看趋势。")
        else:
            st.markdown("### 📈 关键转化率趋势")
            df_trend = pd.DataFrame(trend)

            if len(df_trend) >= 2:
                # CTR趋势
                if df_trend["ctr"].sum() > 0:
                    fig_ctr = go.Figure()
                    fig_ctr.add_trace(go.Scatter(
                        x=df_trend["date"], y=df_trend["ctr"],
                        mode="lines+markers", name="封面点击率(%)",
                        line=dict(color="#533483", width=2),
                    ))
                    fig_ctr.add_hline(y=5, line_dash="dash", line_color="green",
                                      annotation_text="达标线 5%")
                    fig_ctr.update_layout(height=280, template="plotly_white",
                                          title="封面点击率 (CTR) 趋势",
                                          margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_ctr, use_container_width=True)

                # 互动率趋势
                if df_trend["engage_rate"].sum() > 0:
                    fig_eng = go.Figure()
                    fig_eng.add_trace(go.Scatter(
                        x=df_trend["date"], y=df_trend["engage_rate"],
                        mode="lines+markers", name="综合互动率(%)",
                        line=dict(color="#0f3460", width=2),
                    ))
                    fig_eng.add_hline(y=10, line_dash="dash", line_color="green",
                                      annotation_text="达标线 10%")
                    fig_eng.update_layout(height=280, template="plotly_white",
                                          title="综合互动率趋势",
                                          margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_eng, use_container_width=True)

                # 关注转化趋势
                if df_trend["new_followers"].sum() > 0:
                    fig_fol = go.Figure()
                    fig_fol.add_trace(go.Bar(
                        x=df_trend["date"], y=df_trend["new_followers"],
                        name="新增关注",
                        marker_color="#e94560",
                    ))
                    fig_fol.update_layout(height=280, template="plotly_white",
                                          title="新增关注趋势",
                                          margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_fol, use_container_width=True)

            # 历史记录表格
            st.markdown("### 📋 历史记录")
            for r in reversed(get_all_funnel_records()[-10:]):
                scope_icon = "📝" if r.get("scope") == "post" else "📊"
                with st.expander(f"{scope_icon} #{r['id']} {r.get('title', '')}（{r.get('date', '')}）"):
                    cols = st.columns(5)
                    with cols[0]:
                        st.metric("曝光", f"{r.get('impressions', 0):,}")
                    with cols[1]:
                        st.metric("浏览", f"{r.get('views', 0):,}")
                    with cols[2]:
                        st.metric("互动", f"{r.get('total_engagement', 0):,}")
                    with cols[3]:
                        st.metric("主页访问", f"{r.get('profile_visits', 0):,}")
                    with cols[4]:
                        st.metric("新增关注", f"{r.get('new_followers', 0):,}")

    # ===== Tab 4: 后链路指南 =====
    with tab_guide:
        st.markdown("### 📖 后链路完整指南")
        st.markdown("""
        <div class="tip-card">
            <strong>什么是「后链路」？</strong><br>
            后链路 = 用户从看到你的内容到最终成为你的粉丝/客户的完整路径。<br>
            每一步都会有人「流失」，你的目标是找到流失最多的那一步，然后优化它。
        </div>
        """, unsafe_allow_html=True)

        # 漏斗模型说明
        st.markdown("### 🔽 小红书后链路漏斗模型")
        funnel_display = [
            ("📢 曝光", "笔记出现在信息流/搜索中", "取决于：标签精准度、发布时间、账号权重"),
            ("👆 点击", "用户被封面+标题吸引点进来", "取决于：封面图质量、标题吸引力、缩略图效果"),
            ("👀 浏览", "用户看完了内容", "取决于：开头3句话、内容节奏、信息密度"),
            ("❤️ 互动", "用户点赞/收藏/评论/分享", "取决于：内容价值、情感共鸣、互动引导"),
            ("🏠 主页访问", "用户想了解你是谁", "取决于：个人品牌力、评论区专业度、系列感"),
            ("➕ 关注", "用户决定关注你", "取决于：主页简介、内容一致性、置顶笔记质量"),
            ("📱 私域沉淀", "粉丝进入微信/社群", "取决于：私域引导话术、诱饵价值、入群门槛"),
            ("💰 变现", "粉丝成为付费用户", "取决于：产品价值、信任度、定价策略"),
        ]

        for i, (icon, desc, factor) in enumerate(funnel_display):
            width_pct = 100 - i * 8
            color_opacity = 1.0 - i * 0.08
            st.markdown(f"""<div style="
                width:{width_pct}%; margin:0 auto; padding:0.6rem 1rem;
                background:rgba(83,52,131,{color_opacity:.2f}); border-radius:8px;
                margin-bottom:4px; color:#333;
            ">
                <strong>{icon}</strong> {desc}<br>
                <small style="color:#666">{factor}</small>
            </div>""", unsafe_allow_html=True)
            if i < len(funnel_display) - 1:
                st.markdown(f"""<div style="text-align:center; color:#533483; font-size:1.2rem;">▼</div>""",
                            unsafe_allow_html=True)

        st.markdown("---")

        # 各环节详细说明
        st.markdown("### 📊 各环节基准参考值")
        for stage in FUNNEL_STAGES:
            with st.expander(f"{stage['name']}｜{stage['metric_name']}"):
                cols = st.columns(3)
                with cols[0]:
                    st.metric("🔴 偏低", f"<{stage['benchmark_low']}%")
                with cols[1]:
                    st.metric("🟢 达标", f"≥{stage['benchmark_good']}%")
                with cols[2]:
                    st.metric("🌟 优秀", f"≥{stage['benchmark_excellent']}%")
                st.markdown(f"**低转化原因：** {stage['diagnosis_low']}")
                st.markdown("**优化动作：**")
                for action in stage["actions_low"]:
                    st.markdown(f"""<div class="tip-card">{action}</div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🎯 各阶段重点关注的环节")
        for stage_name_ref, info in FUNNEL_HEALTH_BENCHMARKS.items():
            st.markdown(f"""<div class="plan-card">
                <strong>📍 {stage_name_ref}</strong>：重点看
                {'、'.join(info['重点关注'])}<br>
                <small>{info['说明']}</small>
            </div>""", unsafe_allow_html=True)





def _render_funnel_results(funnel_results: list, bottleneck: dict):
    """渲染漏斗分析结果（被多处复用）"""
    # 漏斗可视化
    for r in funnel_results:
        is_bottleneck = r["key"] == bottleneck.get("key", "")
        border = "border:2px solid #e94560;" if is_bottleneck else ""
        badge = " ← 🔴 最大瓶颈" if is_bottleneck else ""

        # 进度条颜色
        bar_color = "#4CAF50" if r["level"] in ("excellent", "good") else "#FF9800" if r["level"] == "normal" else "#f44336"
        bar_width = min(r["rate"] / max(r["benchmark_excellent"], 1) * 100, 100)

        st.markdown(f"""<div class="plan-card" style="{border}">
            <strong>{r['name']}</strong>{badge}<br>
            {r['from_label']} <strong>{r['from_value']:,}</strong> → {r['to_label']} <strong>{r['to_value']:,}</strong><br>
            {r['metric_name']}：<strong style="font-size:1.3rem;">{r['rate']}%</strong> {r['level_label']}
            （基准：{r['benchmark_low']}% ~ {r['benchmark_good']}% ~ {r['benchmark_excellent']}%）
            <div style="background:#eee; border-radius:4px; height:8px; margin-top:6px;">
                <div style="background:{bar_color}; width:{bar_width}%; height:8px; border-radius:4px;"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # 瓶颈详情
    if bottleneck:
        st.markdown("---")
        st.markdown("### 🔴 最大瓶颈诊断")
        st.markdown(f"""<div class="tip-card" style="border-left-color:#e94560">
            <strong>{bottleneck['name']}</strong>：转化率 <strong>{bottleneck['rate']}%</strong>（基准 {bottleneck['benchmark_good']}%）<br>
            <strong>问题：</strong>{bottleneck.get('diagnosis', '')}
        </div>""", unsafe_allow_html=True)

        st.markdown("### ⚡ 立即执行的优化动作")
        for i, action in enumerate(bottleneck.get("actions", []), 1):
            st.markdown(f"""<div class="tip-card"><strong>动作{i}</strong>：{action}</div>""", unsafe_allow_html=True)

    # 各环节亮点
    good_stages = [r for r in funnel_results if r["level"] in ("excellent", "good")]
    if good_stages:
        st.markdown("### 🟢 做得好的环节")
        for r in good_stages:
            st.markdown(f"- ✅ **{r['name']}**：{r['rate']}%（{r['level_label']}）")


# ==================== 页面：合规自查 + 算法解读 ====================



def render_compliance():
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ 合规自查 · 算法解读</h1>
        <p>发布前必查红线 · 算法权重揭秘 · 流量池突破指南 · AI一键合规检测</p>
    </div>
    """, unsafe_allow_html=True)

    tab_check, tab_algo, tab_pool, tab_rules = st.tabs([
        "🔍 AI合规检测",
        "📊 算法权重揭秘",
        "🚀 流量池突破",
        "🚨 平台红线手册",
    ])

    # ===== Tab 1: AI合规检测 =====
    with tab_check:
        st.markdown("### 🔍 发布前AI合规检测")
        st.markdown("""
        <div class="tip-card">
            <strong>⚠️ 平台AI查重+违规检测超严格！</strong>发布前用这个工具自查，避免因小失大。<br>
            检查项：关键词堆砌·原创度·AI标注·绝对化用语·商业导流·搜索SEO
        </div>
        """, unsafe_allow_html=True)

        cc_title = st.text_input("📌 笔记标题", key="cc_title", placeholder="输入你要发布的标题")
        cc_content = st.text_area("📝 笔记正文", height=250, key="cc_content",
                                   placeholder="粘贴你的笔记正文...")
        cc_hashtags = st.text_input("🏷️ 标签（可选）", key="cc_hashtags",
                                     placeholder="#油画 #AI绘画 #当代艺术 ...")
        cc_ai = st.checkbox("🤖 内容使用了AI工具创作（MJ/SD/GPT等）", value=True, key="cc_ai")

        if st.button("🛡️ 开始合规自查", type="primary", use_container_width=True, key="cc_check_btn"):
            if not cc_title and not cc_content:
                st.warning("请至少输入标题或正文")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner("🤖 正在进行合规检测..."):
                    result = generate_compliance_check(cc_title, cc_content, cc_hashtags, cc_ai)
                st.markdown(result)

    # ===== Tab 2: 算法权重揭秘 =====
    with tab_algo:
        st.markdown("### 📊 小红书算法评分权重")
        st.markdown("""
        <div class="tip-card">
            <strong>核心公式：</strong>笔记评分 = 关注×8 + 评论×4 + 转发×4 + 点赞×1 + 收藏×1<br>
            <strong>高分笔记直接优先推送！</strong>所以重点提升「关注」和「评论」，而不是只追求点赞！
        </div>
        """, unsafe_allow_html=True)

        # 权重可视化
        weight_data = []
        for key, info in ALGORITHM_WEIGHTS.items():
            weight_data.append({
                "互动类型": f"{info['emoji']} {info['label']}",
                "权重倍数": info["weight"],
                "说明": info["desc"],
            })

        # 柱状图
        df_w = pd.DataFrame(weight_data)
        fig_w = px.bar(df_w, x="互动类型", y="权重倍数",
                       color="权重倍数",
                       color_continuous_scale=["#e0d6f0", "#533483"],
                       text="权重倍数")
        fig_w.update_layout(height=350, template="plotly_white",
                            showlegend=False,
                            margin=dict(l=20, r=20, t=20, b=40))
        fig_w.update_traces(texttemplate='×%{text}', textposition='outside')
        st.plotly_chart(fig_w, use_container_width=True)

        # 解读
        st.markdown("### 💡 这意味着什么？")
        insights = [
            ("➕ 1个关注 = 8个点赞", "所以每篇笔记结尾加「关注我看更多当代大师🎨」，比写「求点赞」有效8倍"),
            ("💬 1条评论 = 4个点赞", "所以文末必须有互动问题。注意：评论≥15字才算有效互动！"),
            ("🔄 1次转发 = 4个点赞", "做「社交货币」型内容（合集/冷知识/惊喜发现），让人想分享给朋友"),
            ("❤️⭐ 点赞和收藏权重最低", "不要只追求点赞数。10个点赞不如1个关注+1条评论"),
        ]
        for title, desc in insights:
            st.markdown(f"""<div class="plan-card">
                <strong>{title}</strong><br><small>{desc}</small>
            </div>""", unsafe_allow_html=True)

        # 算法评分计算器
        st.markdown("---")
        st.markdown("### 🧮 算法评分计算器")
        st.markdown("_输入你的笔记互动数据，看看算法怎么给你打分_")

        calc_cols = st.columns(5)
        with calc_cols[0]:
            calc_likes = st.number_input("❤️ 点赞", min_value=0, value=50, key="calc_likes")
        with calc_cols[1]:
            calc_saves = st.number_input("⭐ 收藏", min_value=0, value=30, key="calc_saves")
        with calc_cols[2]:
            calc_comments = st.number_input("💬 评论", min_value=0, value=10, key="calc_comments")
        with calc_cols[3]:
            calc_shares = st.number_input("🔄 转发", min_value=0, value=5, key="calc_shares")
        with calc_cols[4]:
            calc_follows = st.number_input("➕ 关注", min_value=0, value=2, key="calc_follows")

        algo_result = calculate_algorithm_score({
            "likes": calc_likes, "saves": calc_saves,
            "comments": calc_comments, "shares": calc_shares,
            "new_followers": calc_follows,
        })

        st.markdown(f"""<div style="text-align:center; padding:1.5rem; background:linear-gradient(135deg, #f8f5ff, #fff); border-radius:16px; border:2px solid #533483;">
            <h2 style="color:#533483; margin:0;">算法评分：{algo_result['raw_score']}</h2>
            <p style="color:#666;">最大贡献项：{algo_result['top_contributor']}</p>
        </div>""", unsafe_allow_html=True)

        # 贡献分解
        st.markdown("**📊 各项贡献分解：**")
        for name, info in algo_result["breakdown"].items():
            pct = round(info["score"] / algo_result["raw_score"] * 100) if algo_result["raw_score"] > 0 else 0
            st.markdown(f"- **{name}**：{info['count']}次 × {info['weight']}倍 = **{info['score']}分**（占{pct}%）")

        # 优化建议
        if algo_result["optimization_priority"]:
            st.markdown("### ⚡ 提分优化建议（投入产出比从高到低）")
            for opt in algo_result["optimization_priority"]:
                st.markdown(f"""<div class="tip-card">
                    <strong>📈 提升「{opt['metric']}」</strong><br>
                    {opt['reason']}<br>
                    <strong>→ 动作：</strong>{opt['action']}
                </div>""", unsafe_allow_html=True)

    # ===== Tab 3: 流量池突破 =====
    with tab_pool:
        st.markdown("### 🚀 流量池突破指南")
        st.markdown("""
        <div class="tip-card">
            <strong>核心机制：</strong>每篇笔记初始曝光200-500。<br>
            只有同时满足 <strong>CTR≥8% + 互动率≥5% + 完读率≥45%</strong> 才能闯进更大流量池！
        </div>
        """, unsafe_allow_html=True)

        # 流量池层级图
        st.markdown("### 📊 流量池层级")
        for i, pool in enumerate(TRAFFIC_POOL_MODEL["pool_levels"]):
            width_pct = 100 - i * 12
            opacity = 1.0 - i * 0.12
            color = "#533483" if i < 2 else "#0f3460" if i < 4 else "#e94560"
            st.markdown(f"""<div style="
                width:{width_pct}%; margin:0 auto; padding:0.8rem 1rem;
                background:rgba({83 if i < 3 else 15},{52 if i < 3 else 52},{131 if i < 3 else 96},{opacity:.15});
                border-left:4px solid {color}; border-radius:0 8px 8px 0;
                margin-bottom:6px;
            ">
                <strong>Level {pool['level']}：曝光 {pool['exposure']}</strong><br>
                <small>突破条件：{pool['condition']}</small><br>
                <small style="color:#533483">→ {pool['action']}</small>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # 流量池突破检测器
        st.markdown("### 🧪 流量池突破检测")
        st.markdown("_输入你的笔记数据，看看能不能突破初始流量池_")

        tp_cols = st.columns(4)
        with tp_cols[0]:
            tp_impr = st.number_input("📢 曝光量", min_value=0, value=300, key="tp_impr")
        with tp_cols[1]:
            tp_views = st.number_input("👀 浏览量", min_value=0, value=0, key="tp_views")
        with tp_cols[2]:
            tp_eng_total = st.number_input("💬 总互动", min_value=0, value=0, key="tp_eng",
                                            help="点赞+收藏+评论+分享总和")
        with tp_cols[3]:
            tp_completion = st.number_input("📖 完读率%", min_value=0, max_value=100, value=0, key="tp_comp",
                                             help="图文不确定可填0跳过")

        if st.button("🚀 检测是否能突破", type="primary", use_container_width=True, key="tp_check"):
            pool_result = analyze_traffic_pool({
                "impressions": tp_impr, "views": tp_views,
                "likes": tp_eng_total // 2, "saves": tp_eng_total // 4,
                "comments": tp_eng_total // 8, "shares": tp_eng_total // 8,
                "completion_rate": tp_completion,
            })

            # 结果展示
            for key, check in pool_result["checks"].items():
                if check["passed"] is None:
                    icon = "⚪"
                    label = "未填写"
                elif check["passed"]:
                    icon = "🟢"
                    label = "达标"
                else:
                    icon = "🔴"
                    label = "未达标"
                st.markdown(f"""<div class="plan-card">
                    {icon} <strong>{check['label']}</strong>：{check['value']}{check['unit']}
                    （需≥{check['threshold']}{check['unit']}）{label}
                </div>""", unsafe_allow_html=True)

            pool = pool_result["current_pool"]
            if pool_result["can_breakthrough"]:
                st.success(f"✅ 恭喜！数据达标，预计可进入 Level {pool['level']}（曝光{pool['exposure']}）")
            else:
                st.error(f"❌ 暂时无法突破。当前预计在 Level {pool['level']}（曝光{pool['exposure']}）")

            if pool_result["breakthrough_actions"]:
                st.markdown("### ⚡ 突破建议")
                for action in pool_result["breakthrough_actions"]:
                    st.markdown(f"""<div class="tip-card">{action}</div>""", unsafe_allow_html=True)

        # 信用分
        st.markdown("---")
        st.markdown("### 📋 信用分体系")
        st.markdown(f"""<div class="tip-card">
            <strong>⚠️ 信用分≥{CREDIT_SCORE_RULES['threshold']}才能解锁流量加持！</strong>
        </div>""", unsafe_allow_html=True)

        for level in CREDIT_SCORE_RULES["levels"]:
            st.markdown(f"""<div class="plan-card">
                <strong>{level['label']} ({level['range']}分)</strong>：{level['effect']}
            </div>""", unsafe_allow_html=True)

        st.markdown("**📈 信用分提升方法：**")
        for tip in CREDIT_SCORE_RULES["gain_tips"]:
            st.markdown(f"- ✅ {tip}")

    # ===== Tab 4: 平台红线手册 =====
    with tab_rules:
        st.markdown("### 🚨 平台红线手册 · 绝对不能碰")
        st.markdown(f"""<div class="tip-card" style="border-left-color:#e94560">
            <strong>⚠️ 核心原则：{CONTENT_GOLDEN_RULES['priority']}</strong><br>
            现在平台AI查重+违规检测超严格，别心存侥幸！
        </div>""", unsafe_allow_html=True)

        for rule in PLATFORM_RED_LINES:
            with st.expander(f"{rule['severity']} {rule['rule']}", expanded=(rule["severity"] == "🔴 严重")):
                st.markdown(f"**{rule['desc']}**")
                st.markdown(f"_处罚：{rule['penalty']}_")
                st.markdown(f"**详情：** {rule['detail']}")
                st.markdown("**自查清单：**")
                for cp in rule["check_points"]:
                    st.markdown(f"- ☐ {cp}")

        st.markdown("---")
        st.markdown("### 📖 内容创作黄金法则")
        for rule_info in CONTENT_GOLDEN_RULES["rules"]:
            st.markdown(f"""<div class="plan-card">
                <strong>📌 {rule_info['rule']}</strong><br>
                {rule_info['desc']}<br>
                <strong>→ 执行：</strong>{rule_info['action']}
            </div>""", unsafe_allow_html=True)


# ==================== 页面：经验宝库 ====================


