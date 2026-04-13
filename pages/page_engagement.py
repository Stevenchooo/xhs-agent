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



def render_engagement_patrol():
    st.markdown("""
    <div class="main-header">
        <h1>💬 互动任务站</h1>
        <p>每天20分钟 · 定额评论 + 回复管理 + 互动数据追踪</p>
    </div>
    """, unsafe_allow_html=True)

    account = get_account_info()
    followers = account.get("followers", 0) if account else 0
    stage_name = "冷启动期" if followers < 1000 else "成长期" if followers < 10000 else "爆发期"
    quota = DAILY_ENGAGEMENT_QUOTA.get(stage_name, DAILY_ENGAGEMENT_QUOTA["冷启动期"])
    today_eng = get_today_engagement()
    streak = get_engagement_streak()

    # 今日进度
    comments_done = today_eng.get("comments", 0)
    comments_target = quota["comments_target"]
    progress = min(comments_done / comments_target * 100, 100) if comments_target > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <h3>{comments_done}/{comments_target}</h3><p>💬 今日评论进度</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <h3>{today_eng.get('replies', 0)}</h3><p>↩️ 今日回复数</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <h3>{streak}天</h3><p>🔥 连续互动天数</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <h3>{round(progress)}%</h3><p>📊 今日完成度</p>
        </div>""", unsafe_allow_html=True)

    # 进度条
    st.progress(progress / 100)
    if progress >= 100:
        st.success("🎉 今日互动任务已完成！")
    elif progress >= 50:
        st.info(f"加油！还差 {comments_target - comments_done} 条评论完成今日目标")
    else:
        st.warning(f"今日还需评论 {comments_target - comments_done} 条")

    st.markdown("---")

    tab_patrol, tab_comments, tab_replies, tab_log, tab_history = st.tabs([
        "🎯 巡逻指南",
        "🤖 批量出评论",
        "↩️ 回复助手",
        "📝 记录互动",
        "📊 互动历史",
    ])

    # ===== Tab 1: 巡逻指南 =====
    with tab_patrol:
        st.markdown(f"### 🎯 {stage_name}·互动巡逻指南")

        st.markdown(f"""<div class="plan-card">
            <strong>📊 今日配额：</strong>{comments_target}条评论 · {quota['daily_time']} · 最佳时间{quota['best_time']}<br>
            <strong>🎯 目标笔记：</strong>{quota['target_post_criteria']}<br>
            <strong>🔍 搜索关键词：</strong>{' · '.join(quota['search_keywords'])}
        </div>""", unsafe_allow_html=True)

        st.markdown("**💡 执行要点：**")
        for tip in quota["tips"]:
            st.markdown(f"""<div class="tip-card">{tip}</div>""", unsafe_allow_html=True)

        st.markdown("### 📋 巡逻SOP（每天照着做）")
        sop_steps = [
            "1️⃣ 打开小红书 → 搜索关键词（油画/当代艺术/AI绘画）",
            "2️⃣ 筛选目标笔记：点赞100-2000，发布24h内",
            "3️⃣ 看笔记内容，找到可以补充信息/分享观点的角度",
            "4️⃣ 用下面的「批量出评论」功能生成评论模板",
            "5️⃣ 稍作修改后发布（不要原封不动复制）",
            "6️⃣ 完成后在「📝 记录互动」Tab记录今日互动",
        ]
        for step in sop_steps:
            st.markdown(f"**{step}**")

    # ===== Tab 2: 批量出评论 =====
    with tab_comments:
        st.markdown("### 🤖 AI批量生成巡逻评论")

        col1, col2 = st.columns(2)
        with col1:
            eg_scenario = st.selectbox("📋 互动场景", [
                "画家介绍类笔记下面评论",
                "AI绘画作品分享下面评论",
                "艺术科普/干货类笔记下面评论",
                "绘画教程下面评论",
                "美术馆/展览分享下面评论",
                "色彩/设计/美学相关下面评论",
            ], key="eg_scenario")
        with col2:
            eg_count = st.slider("生成数量", 3, 8, 5, key="eg_count")

        eg_keywords = st.text_input("🔍 补充关键词（可选）",
                                     placeholder="例如：Richter、油画质感、印象派...",
                                     key="eg_keywords")

        if OPENAI_API_KEY:
            if st.button("🤖 生成巡逻评论", type="primary", use_container_width=True, key="gen_patrol_btn"):
                kw_list = [k.strip() for k in eg_keywords.split("、") if k.strip()] if eg_keywords else quota["search_keywords"]
                with st.spinner("🤖 正在生成巡逻评论..."):
                    result = generate_engagement_batch(eg_scenario, kw_list, eg_count)
                st.success("✅ 评论生成完成！稍作修改后使用")
                st.markdown(result)
        else:
            st.info("💡 配置 Claude API Key 后即可一键生成巡逻评论。")

    # ===== Tab 3: 回复助手 =====
    with tab_replies:
        st.markdown("### ↩️ AI回复建议生成器")
        st.markdown("""
        <div class="tip-card">
            把粉丝的评论粘贴进来，AI帮你生成高质量回复。
            好的回复能引发二次互动，让评论区更活跃。
        </div>
        """, unsafe_allow_html=True)

        reply_input = st.text_area("📝 粘贴收到的评论（每条一行）",
                                    height=150,
                                    placeholder="评论1：太好看了，请问用的什么工具？\n评论2：Richter的画我也很喜欢...\n评论3：求教程！",
                                    key="reply_input")

        if OPENAI_API_KEY:
            if st.button("🤖 生成回复建议", type="primary", use_container_width=True, key="gen_replies_btn"):
                if not reply_input:
                    st.warning("请粘贴评论内容")
                else:
                    with st.spinner("🤖 正在生成回复建议..."):
                        result = generate_reply_suggestions(reply_input)
                    st.success("✅ 回复建议生成完成！")
                    st.markdown(result)
        else:
            st.info("💡 配置 Claude API Key 后即可自动生成高质量回复建议。")

    # ===== Tab 4: 记录互动 =====
    with tab_log:
        st.markdown("### 📝 记录今日互动")

        col1, col2, col3 = st.columns(3)
        with col1:
            log_type = st.selectbox("互动类型", [
                "comment（评论引流）",
                "reply（回复粉丝）",
                "dm（私信互动）",
            ], key="log_type")
        with col2:
            log_target = st.text_input("目标笔记/用户", key="log_target",
                                        placeholder="简单描述：如「油画合集笔记」")
        with col3:
            log_note = st.text_input("备注", key="log_note",
                                      placeholder="如：留了专业评论，分享了Richter知识")

        if st.button("📝 记录此次互动", type="primary", use_container_width=True, key="log_eng_btn"):
            actual_type = log_type.split("（")[0]
            log_engagement({
                "type": actual_type,
                "target": log_target,
                "note": log_note,
            })
            st.success("✅ 互动已记录！")
            st.rerun()

        # 快速记录按钮
        st.markdown("#### ⚡ 快速记录")
        quick_cols = st.columns(3)
        with quick_cols[0]:
            if st.button("💬 记录1条评论", use_container_width=True, key="quick_comment"):
                log_engagement({"type": "comment", "target": "快速记录", "note": ""})
                st.success("✅ +1评论")
                st.rerun()
        with quick_cols[1]:
            if st.button("↩️ 记录1条回复", use_container_width=True, key="quick_reply"):
                log_engagement({"type": "reply", "target": "快速记录", "note": ""})
                st.success("✅ +1回复")
                st.rerun()
        with quick_cols[2]:
            if st.button("📩 记录1次私信", use_container_width=True, key="quick_dm"):
                log_engagement({"type": "dm", "target": "快速记录", "note": ""})
                st.success("✅ +1私信")
                st.rerun()

        # 今日明细
        if today_eng.get("logs"):
            st.markdown("#### 📋 今日互动明细")
            for log in reversed(today_eng["logs"]):
                time_str = log.get("timestamp", "")[-8:-3] if log.get("timestamp") else ""
                type_emoji = {"comment": "💬", "reply": "↩️", "dm": "📩"}.get(log.get("type", ""), "📌")
                st.markdown(f"- {type_emoji} `{time_str}` {log.get('target', '')} {log.get('note', '')}")

    # ===== Tab 5: 互动历史 =====
    with tab_history:
        st.markdown("### 📊 互动数据历史")
        history = get_engagement_history(14)

        if not any(h.get("total", 0) > 0 for h in history):
            st.info("暂无互动记录。开始在「📝 记录互动」Tab记录你的每日互动。")
        else:
            # 数据表格
            hist_data = []
            for h in history:
                hist_data.append({
                    "日期": h["date"],
                    "总互动": h.get("total", 0),
                    "评论": h.get("comments", 0),
                    "回复": h.get("replies", 0),
                })
            df_hist = pd.DataFrame(hist_data)
            st.dataframe(df_hist, use_container_width=True, hide_index=True)

            # 趋势图
            if len(hist_data) > 1:
                fig = px.bar(
                    df_hist, x="日期", y=["评论", "回复"],
                    barmode="stack",
                    color_discrete_sequence=["#533483", "#0f3460"],
                )
                fig.update_layout(height=300, template="plotly_white",
                                  margin=dict(l=20, r=20, t=20, b=40))
                st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"🔥 **当前连续互动天数：{streak}天**")
            if streak >= 7:
                st.success("太棒了！连续7天以上的互动是涨粉的关键！")
            elif streak >= 3:
                st.info("不错！继续保持，目标连续7天！")
            else:
                st.warning("互动是涨粉最有效的手段之一，坚持每天做！")


# ==================== 页面：账号体检 ====================



def render_engagement():
    st.markdown("""
    <div class="main-header">
        <h1>💬 评论引流工作台</h1>
        <p>高质量评论 = 精准引流 · 每天20分钟 · 日均涨粉5-15个</p>
    </div>
    """, unsafe_allow_html=True)

    tab_gen, tab_templates, tab_guide = st.tabs([
        "🤖 AI生成评论",
        "📋 评论话术库",
        "📖 引流指南",
    ])

    # ==================== Tab 1: AI生成评论 ====================
    with tab_gen:
        st.markdown("### 🤖 AI生成高质量评论")
        st.markdown("""
        <div class="tip-card">
            <strong>用法：</strong>告诉我你要评论的笔记类型和主题，我帮你生成5条专业评论。
            每条都自带"专业人设"，让其他看到的人想点进你主页。
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            c_type = st.selectbox("📋 笔记类型", [
                "画家介绍/艺术科普",
                "AI绘画/AI作品分享",
                "油画作品赏析",
                "绘画教程/技法分享",
                "艺术展览/拍卖资讯",
                "色彩/设计/美学",
                "其他艺术相关",
            ], key="c_type")
        with col2:
            c_count = st.slider("生成数量", 3, 8, 5, key="c_count")

        c_topic = st.text_input("📌 笔记具体主题/标题",
                                 placeholder="例如：Gerhard Richter的作品赏析 / 用AI画了一组油画",
                                 key="c_topic")

        if st.button("🤖 生成评论", type="primary", use_container_width=True, key="gen_comment_btn"):
            if not c_topic:
                st.warning("请输入笔记主题")
            elif not OPENAI_API_KEY:
                st.error(AI_SETUP_ERROR)
            else:
                with st.spinner("🤖 正在生成高质量评论..."):
                    result = generate_engagement_comments(c_type, c_topic, c_count)
                st.success("✅ 评论生成完成！复制去小红书使用")
                st.markdown(result)

                st.markdown("---")
                st.markdown("""
                <div class="tip-card">
                    <strong>💡 使用提示：</strong><br>
                    1. 不要原封不动复制——稍微改几个字让它更自然<br>
                    2. 每天控制在5-8条，太多会被系统限流<br>
                    3. 优先评论1小时内发布的新笔记（新笔记更容易上热评）<br>
                    4. 最佳评论时间：21:00-23:00（用户活跃高峰）
                </div>
                """, unsafe_allow_html=True)

    # ==================== Tab 2: 评论话术库 ====================
    with tab_templates:
        st.markdown("### 📋 评论话术模板库")
        st.markdown("_按场景分类的评论模板，填空即用。括号{}内为可替换内容_")

        for scene, templates in COMMENT_TEMPLATES.items():
            with st.expander(f"💬 {scene}（{len(templates)}条模板）", expanded=False):
                for i, tpl in enumerate(templates, 1):
                    st.markdown(f"""<div class="plan-card">
                        <strong>模板{i}</strong><br>
                        {tpl}
                    </div>""", unsafe_allow_html=True)

    # ==================== Tab 3: 引流指南 ====================
    with tab_guide:
        st.markdown("### 📖 评论区引流完整指南")
        st.markdown("_每天20分钟，精准引流日均5-15个关注_")

        guides = [
            {
                "title": "🎯 选对目标笔记",
                "content": [
                    "搜索关键词：「油画」「当代艺术」「AI绘画」「画家」「艺术科普」",
                    "选择条件：点赞500+且发布时间在24小时内的笔记",
                    "优先评论：和你领域高度相关的内容（画家介绍/AI作品/艺术科普）",
                    "避免评论：已经有100+评论的笔记（你的评论会被淹没）",
                ],
            },
            {
                "title": "✍️ 写出高质量评论",
                "content": [
                    "❌ 错误示范：「好好看」「太棒了」「收藏了」→ 这种评论零价值",
                    "✅ 正确示范：分享补充知识、个人经验、专业观点、提出好问题",
                    "🔑 关键原则：让别人看到你的评论后觉得「这个人很懂」→ 点进主页",
                    "📏 长度：50-150字，太短没价值，太长像打广告",
                ],
            },
            {
                "title": "⏰ 最佳时间节奏",
                "content": [
                    "每天固定20分钟：建议21:00-21:20",
                    "每天评论5-8条（不要超过10条，会触发限流）",
                    "优先回复新笔记（发布1-3小时内的）",
                    "周末可以增加到10-12条（周末用户更活跃）",
                ],
            },
            {
                "title": "📊 效果追踪",
                "content": [
                    "记录每天的评论数量和新增关注数",
                    "一周后复盘：哪种评论转化率最高？",
                    "好的评论引流率约3-5%（每100个看到的人有3-5个关注你）",
                    "坚持30天，预计通过评论引流100-300个精准粉丝",
                ],
            },
        ]

        for guide in guides:
            with st.expander(guide["title"], expanded=True):
                for item in guide["content"]:
                    st.markdown(f"- {item}")


# ==================== 页面：竞品雷达 ====================



def render_post_tracking():
    st.markdown("""
    <div class="main-header">
        <h1>⏱️ 发后跟踪器</h1>
        <p>发布后 1小时 → 24小时 → 72小时 三个检查点 · 用数据驱动优化</p>
    </div>
    """, unsafe_allow_html=True)

    tab_new, tab_active, tab_history = st.tabs([
        "🆕 开始追踪",
        "📊 进行中",
        "📋 历史记录",
    ])

    # ===== Tab 1: 开始追踪 =====
    with tab_new:
        st.markdown("### 🆕 刚发布了一篇笔记？开始追踪！")
        st.markdown("""
        <div class="tip-card">
            <strong>📌 使用方法：</strong>发布笔记后，在这里填写标题和类型，开始追踪。
            然后在1小时、24小时、72小时后分别回来录入数据，AI会帮你评估表现。
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            tk_title = st.text_input("📌 笔记标题", key="tk_title", placeholder="填写刚发布的笔记标题")
        with col2:
            tk_type = st.selectbox("📋 内容类型", list(CONTENT_TYPES.keys()), key="tk_type")

        if st.button("🚀 开始追踪", type="primary", use_container_width=True, key="start_tracking"):
            if not tk_title:
                st.warning("请输入笔记标题")
            else:
                tracking_id = start_post_tracking({
                    "title": tk_title,
                    "content_type": tk_type,
                })
                st.success(f"✅ 开始追踪！ID: {tracking_id}")
                st.markdown(f"""<div class="tip-card">
                    <strong>⏰ 接下来：</strong><br>
                    • 发布后 <strong>1小时</strong>：回来录入第一次数据<br>
                    • 发布后 <strong>24小时</strong>：录入第二次数据<br>
                    • 发布后 <strong>72小时</strong>：录入最终数据
                </div>""", unsafe_allow_html=True)

        # 展示检查点基准
        st.markdown("### 📊 各检查点达标基准")
        for cp_key, cp_info in POST_CHECKPOINTS.items():
            with st.expander(f"{cp_info['label']}（发布后{cp_info['time_hours']}小时）"):
                st.markdown(f"**{cp_info['description']}**")
                benchmarks = cp_info["benchmarks"]
                cols = st.columns(4)
                with cols[0]:
                    st.metric("浏览", f"≥{benchmarks['views']}")
                with cols[1]:
                    st.metric("点赞", f"≥{benchmarks['likes']}")
                with cols[2]:
                    st.metric("收藏", f"≥{benchmarks['saves']}")
                with cols[3]:
                    st.metric("评论", f"≥{benchmarks['comments']}")

    # ===== Tab 2: 进行中 =====
    with tab_active:
        active = get_active_tracking()
        if not active:
            st.info("暂无正在追踪的笔记。去「🆕 开始追踪」Tab添加新的追踪。")
        else:
            for t in active:
                pub_time = t.get("publish_time", "")
                hours_ago = 0
                if pub_time:
                    pub_dt = datetime.datetime.fromisoformat(pub_time)
                    hours_ago = (datetime.datetime.now() - pub_dt).total_seconds() / 3600

                checked = t.get("checkpoints", {})
                with st.expander(
                    f"📊 #{t['id']} 「{t.get('title', '')}」· 发布{hours_ago:.0f}小时前",
                    expanded=True,
                ):
                    # 检查点进度条
                    progress_cols = st.columns(3)
                    for i, (cp_key, cp_info) in enumerate(POST_CHECKPOINTS.items()):
                        with progress_cols[i]:
                            done = cp_key in checked
                            icon = "✅" if done else "⏳" if hours_ago >= cp_info["time_hours"] else "🔜"
                            result = checked.get(cp_key, {}).get("overall", "")
                            color = "🟢" if result == "good" else "🔴" if result == "needs_attention" else ""
                            st.markdown(f"**{icon} {cp_info['label']}** {color}")

                    # 录入数据区域
                    st.markdown("---")
                    next_cp = None
                    for cp_key in POST_CHECKPOINTS:
                        if cp_key not in checked:
                            next_cp = cp_key
                            break

                    if next_cp:
                        cp_info = POST_CHECKPOINTS[next_cp]
                        st.markdown(f"### 📝 录入 {cp_info['label']} 数据")

                        cp_cols = st.columns(4)
                        with cp_cols[0]:
                            cp_views = st.number_input("👀 浏览", min_value=0, key=f"cp_v_{t['id']}_{next_cp}")
                        with cp_cols[1]:
                            cp_likes = st.number_input("❤️ 点赞", min_value=0, key=f"cp_l_{t['id']}_{next_cp}")
                        with cp_cols[2]:
                            cp_saves = st.number_input("⭐ 收藏", min_value=0, key=f"cp_s_{t['id']}_{next_cp}")
                        with cp_cols[3]:
                            cp_comments = st.number_input("💬 评论", min_value=0, key=f"cp_c_{t['id']}_{next_cp}")

                        if st.button(f"📊 提交{cp_info['label']}数据", type="primary",
                                     use_container_width=True, key=f"submit_cp_{t['id']}_{next_cp}"):
                            metrics = {
                                "views": cp_views,
                                "likes": cp_likes,
                                "saves": cp_saves,
                                "comments": cp_comments,
                            }
                            result = record_checkpoint(t["id"], next_cp, metrics)

                            status_emoji = "🟢" if result["status"] == "good" else "🔴"
                            st.markdown(f"### {status_emoji} {cp_info['label']} 结果")

                            for metric, info in result["details"].items():
                                bar = "✅" if info["passed"] else "❌"
                                st.markdown(f"- {bar} **{metric}**: {info['actual']} / 目标{info['target']}（{info['ratio']}%）")

                            st.markdown("### ⚡ 建议行动")
                            for action in result["actions"]:
                                st.markdown(f"""<div class="tip-card">{action}</div>""", unsafe_allow_html=True)

                            # AI分析
                            if OPENAI_API_KEY:
                                with st.spinner("🤖 AI正在分析..."):
                                    analysis = generate_post_performance_analysis(t, next_cp, result)
                                st.markdown("### 🤖 AI分析")
                                st.markdown(analysis)
                    else:
                        st.success("✅ 所有检查点已完成！")

                    # 展示已有检查点的数据
                    if checked:
                        st.markdown("### 📈 已完成检查点")
                        for cp_key, cp_data in checked.items():
                            cp_label = POST_CHECKPOINTS[cp_key]["label"]
                            overall = "🟢 达标" if cp_data.get("overall") == "good" else "🔴 需关注"
                            m = cp_data.get("metrics", {})
                            st.markdown(f"**{cp_label}** {overall}：浏览{m.get('views', 0)} 点赞{m.get('likes', 0)} 收藏{m.get('saves', 0)} 评论{m.get('comments', 0)}")

    # ===== Tab 3: 历史记录 =====
    with tab_history:
        all_tracking = get_all_tracking()
        completed = [t for t in all_tracking if t.get("status") == "completed"]
        if not completed:
            st.info("暂无已完成的追踪记录。")
        else:
            st.markdown(f"共完成 **{len(completed)}** 次追踪")
            for t in reversed(completed):
                checked = t.get("checkpoints", {})
                final = checked.get("72h", {})
                final_m = final.get("metrics", {})
                final_status = "🟢" if final.get("overall") == "good" else "🔴"
                with st.expander(f"{final_status} #{t['id']} 「{t.get('title', '')}」"):
                    for cp_key, cp_data in checked.items():
                        cp_label = POST_CHECKPOINTS[cp_key]["label"]
                        m = cp_data.get("metrics", {})
                        overall = "✅" if cp_data.get("overall") == "good" else "❌"
                        st.markdown(f"**{cp_label}** {overall}：浏览{m.get('views', 0)} 点赞{m.get('likes', 0)} 收藏{m.get('saves', 0)} 评论{m.get('comments', 0)}")


# ==================== 页面：互动任务站 ====================


