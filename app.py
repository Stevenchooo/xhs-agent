"""
🎨 小红书运营Agent - 游戏IP真人化·童年角色短视频 智能运营助手
游戏角色真人化 × 童年IP短视频 × 智能内容运营
"""

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

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="🎨 游戏IP真人化·童年角色短视频 运营Agent",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义样式（赛博朋克科技感） ====================
st.markdown("""
<style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@400;600&display=swap');

    /* ── CSS 变量 ── */
    :root {
        --cyan: #00f5ff;
        --purple: #bd00ff;
        --green: #00ff87;
        --pink: #ff0099;
        --dark: #020408;
        --dark2: #060d14;
        --dark3: #0a1628;
        --glass: rgba(255,255,255,0.03);
        --glass-border: rgba(0,245,255,0.12);
        --text: #e2e8f0;
        --text-dim: #8fa3bb;
    }

    /* ── 全局 ── */
    html, body, .stApp {
        background-color: var(--dark) !important;
        background-image:
            linear-gradient(rgba(0,245,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,245,255,0.03) 1px, transparent 1px) !important;
        background-size: 60px 60px !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stApp { background-attachment: fixed !important; }

    /* selection */
    ::selection { background: var(--cyan); color: var(--dark); }

    /* scrollbar */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: var(--dark2); }
    ::-webkit-scrollbar-thumb { background: var(--cyan); border-radius: 4px; }

    /* ── 顶部进度条（Streamlit loading bar）── */
    div[data-testid="stStatusWidget"] { display: none; }

    /* ── 侧边栏 ── */
    div[data-testid="stSidebar"] {
        background: var(--dark2) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    div[data-testid="stSidebar"] * { color: var(--text) !important; }
    div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3 {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--cyan) !important;
        letter-spacing: 0.05em;
        font-size: 0.95rem !important;
    }
    /* 侧边栏 radio */
    div[data-testid="stSidebar"] label {
        color: #b8c7d9 !important;
        font-size: 0.85rem !important;
        padding: 4px 0 !important;
        transition: color 0.2s !important;
    }
    div[data-testid="stSidebar"] label:hover { color: var(--cyan) !important; }
    div[data-testid="stSidebar"] [data-baseweb="radio"] [aria-checked="true"] ~ div {
        color: var(--cyan) !important;
    }
    /* 侧边栏分隔线 */
    div[data-testid="stSidebar"] hr {
        border-color: rgba(0,245,255,0.1) !important;
        margin: 12px 0 !important;
    }
    /* 侧边栏 caption */
    div[data-testid="stSidebar"] small,
    div[data-testid="stSidebar"] .stCaption p {
        color: var(--text-dim) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
    }

    /* ── 主内容区 ── */
    section[data-testid="stMain"] > div {
        padding-top: 1.5rem !important;
    }

    /* ── 标题 h1-h3 ── */
    h1, h2, h3 { color: var(--text) !important; }
    h1 { font-size: 1.8rem !important; font-weight: 800 !important; letter-spacing: -0.01em !important; }
    h3 { font-size: 1.05rem !important; font-weight: 600 !important; }

    /* ── 按钮 ── */
    .stButton > button {
        background: transparent !important;
        border: 1.5px solid var(--cyan) !important;
        color: var(--cyan) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.06em !important;
        border-radius: 2px !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.25s !important;
        box-shadow: 0 0 10px rgba(0,245,255,0.1) !important;
    }
    .stButton > button:hover {
        background: var(--cyan) !important;
        color: var(--dark) !important;
        box-shadow: 0 0 24px rgba(0,245,255,0.4) !important;
        transform: translateY(-1px) !important;
    }
    /* primary button variant */
    .stButton > button[kind="primary"] {
        background: var(--cyan) !important;
        color: var(--dark) !important;
        font-weight: 700 !important;
        box-shadow: 0 0 20px rgba(0,245,255,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 40px rgba(0,245,255,0.6) !important;
    }

    /* ── 输入框 ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: var(--dark3) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 2px !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        transition: border-color 0.3s, box-shadow 0.3s !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--cyan) !important;
        box-shadow: 0 0 16px rgba(0,245,255,0.1) !important;
    }
    .stTextInput label, .stTextArea label, .stNumberInput label,
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stDateInput label, .stTimeInput label {
        color: var(--text-dim) !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--dark3) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 2px !important;
        color: var(--text) !important;
    }
    .stSelectbox > div > div:focus-within,
    .stMultiSelect > div > div:focus-within {
        border-color: var(--cyan) !important;
        box-shadow: 0 0 12px rgba(0,245,255,0.1) !important;
    }

    /* ── Code blocks ── */
    code, .stCodeBlock {
        background: var(--dark3) !important;
        border: 1px solid rgba(0,245,255,0.1) !important;
        border-radius: 2px !important;
        color: var(--cyan) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.82rem !important;
    }
    .stCodeBlock { padding: 1rem !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] details summary,
    [data-testid="stExpander"] details > summary {
        background: var(--dark3) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 2px !important;
        color: var(--text) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: border-color 0.3s !important;
    }
    .streamlit-expanderHeader:hover,
    [data-testid="stExpander"] details summary:hover {
        border-color: var(--cyan) !important;
        color: var(--cyan) !important;
    }
    /* expander header text in newer Streamlit */
    [data-testid="stExpander"] details summary p,
    [data-testid="stExpander"] summary span {
        color: var(--text) !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderContent,
    [data-testid="stExpander"] details > div {
        background: rgba(6,13,20,0.6) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-top: none !important;
        border-radius: 0 0 2px 2px !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid rgba(0,245,255,0.1) !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-dim) !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        border-radius: 0 !important;
        border-bottom: 2px solid transparent !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.2s !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--cyan) !important;
        border-bottom-color: var(--cyan) !important;
        background: transparent !important;
        text-shadow: 0 0 12px rgba(0,245,255,0.4) !important;
    }

    /* ── Metric ── */
    div[data-testid="stMetric"] {
        background: var(--glass) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 2px !important;
        padding: 1rem 1.2rem !important;
        position: relative !important;
    }
    div[data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    }
    div[data-testid="stMetricLabel"] p {
        color: var(--text-dim) !important;
        font-size: 0.72rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetricValue"] {
        color: var(--cyan) !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        font-family: 'JetBrains Mono', monospace !important;
        text-shadow: 0 0 20px rgba(0,245,255,0.3) !important;
    }
    div[data-testid="stMetricDelta"] {
        color: var(--green) !important;
        font-size: 0.8rem !important;
    }

    /* ── Info / Success / Warning / Error ── */
    div[data-testid="stInfo"] {
        background: rgba(0,245,255,0.04) !important;
        border: 1px solid rgba(0,245,255,0.2) !important;
        border-radius: 2px !important;
        color: var(--text) !important;
    }
    div[data-testid="stSuccess"] {
        background: rgba(0,255,135,0.04) !important;
        border: 1px solid rgba(0,255,135,0.2) !important;
        border-radius: 2px !important;
        color: var(--text) !important;
    }
    div[data-testid="stWarning"] {
        background: rgba(255,200,0,0.04) !important;
        border: 1px solid rgba(255,200,0,0.2) !important;
        border-radius: 2px !important;
        color: var(--text) !important;
    }
    div[data-testid="stError"] {
        background: rgba(255,68,102,0.04) !important;
        border: 1px solid rgba(255,68,102,0.2) !important;
        border-radius: 2px !important;
        color: var(--text) !important;
    }

    /* ── 分隔线 ── */
    hr {
        border-color: rgba(0,245,255,0.08) !important;
        margin: 1.2rem 0 !important;
    }

    /* ── Dataframe / Table ── */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(0,245,255,0.1) !important;
        border-radius: 2px !important;
    }

    /* ── Progress bar ── */
    div[data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, var(--cyan), var(--purple)) !important;
        box-shadow: 0 0 8px rgba(0,245,255,0.4) !important;
    }

    /* ─────────────────────────────────────────
       自定义组件样式
    ───────────────────────────────────────── */

    /* 页面主标题横幅 */
    .main-header {
        background: var(--dark3);
        padding: 1.6rem 2rem;
        border-radius: 2px;
        margin-bottom: 1.5rem;
        text-align: center;
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--cyan), var(--purple), transparent);
    }
    .main-header::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(0,245,255,0.04) 0%, transparent 60%);
        pointer-events: none;
    }
    .main-header h1 {
        color: var(--text) !important;
        margin: 0;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.01em;
    }
    .main-header h1 span { color: var(--cyan); text-shadow: 0 0 20px rgba(0,245,255,0.4); }
    .main-header p {
        color: var(--text-dim);
        margin: 0.5rem 0 0;
        font-size: 0.9rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.04em;
    }

    /* 数据卡片 */
    .metric-card {
        background: var(--glass);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 2px;
        padding: 1.2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: border-color 0.3s, box-shadow 0.3s;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    }
    .metric-card:hover {
        border-color: rgba(0,245,255,0.25);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 0 20px rgba(0,245,255,0.04);
    }
    .metric-card h3 {
        color: var(--cyan) !important;
        font-size: 2rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 900 !important;
        margin: 0;
        text-shadow: 0 0 16px rgba(0,245,255,0.3);
    }
    .metric-card p { color: var(--text-dim); margin: 0.3rem 0 0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; font-family: 'JetBrains Mono', monospace; }

    /* 阶段徽章 */
    .stage-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: transparent;
        border: 1.5px solid var(--cyan);
        color: var(--cyan);
        padding: 0.25rem 0.9rem;
        border-radius: 2px;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
        box-shadow: 0 0 12px rgba(0,245,255,0.15);
    }

    /* 提示卡片 */
    .tip-card {
        background: rgba(0,245,255,0.03);
        border-left: 3px solid var(--cyan);
        border-top: 1px solid rgba(0,245,255,0.1);
        border-right: 1px solid rgba(0,245,255,0.05);
        border-bottom: 1px solid rgba(0,245,255,0.05);
        padding: 0.9rem 1rem;
        border-radius: 0 2px 2px 0;
        margin: 0.5rem 0;
        color: var(--text);
        font-size: 0.87rem;
        line-height: 1.6;
    }
    .tip-card strong { color: var(--cyan); }

    /* 时间徽章 */
    .time-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(0,245,255,0.08);
        border: 1px solid rgba(0,245,255,0.25);
        color: var(--cyan);
        padding: 0.2rem 0.7rem;
        border-radius: 2px;
        font-size: 0.78rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.08em;
        box-shadow: 0 0 8px rgba(0,245,255,0.1);
    }

    /* 计划卡片 */
    .plan-card {
        background: var(--dark3);
        border-radius: 2px;
        padding: 0.9rem 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.06);
        color: var(--text);
        font-size: 0.87rem;
        line-height: 1.6;
        transition: border-color 0.3s;
    }
    .plan-card:hover { border-color: rgba(0,245,255,0.15); }
    .plan-card strong { color: var(--text); }

    /* 选题卡片 */
    .topic-card {
        background: var(--glass);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 2px;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        cursor: pointer;
        transition: all 0.25s;
        color: var(--text);
        font-size: 0.87rem;
        position: relative;
        overflow: hidden;
    }
    .topic-card::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        background: var(--cyan);
        transform: scaleY(0);
        transition: transform 0.3s;
    }
    .topic-card:hover {
        border-color: rgba(0,245,255,0.25);
        background: rgba(0,245,255,0.03);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        padding-left: 1.3rem;
    }
    .topic-card:hover::before { transform: scaleY(1); }

    /* 画家徽章 */
    .artist-badge {
        display: inline-block;
        background: rgba(0,245,255,0.08);
        border: 1px solid rgba(0,245,255,0.2);
        color: var(--cyan);
        padding: 0.15rem 0.6rem;
        border-radius: 2px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        margin: 0.2rem;
        letter-spacing: 0.04em;
    }

    /* ── Plotly charts dark mode ── */
    .js-plotly-plot .plotly .modebar { background: var(--dark3) !important; }

    /* ── 隐藏 Streamlit 底部 footer ── */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


def ai_enabled() -> bool:
    """Whether AI-dependent features are currently available."""
    return cfg.has_ai_config()


class _DynamicAIGate:
    """Allow legacy `if OPENAI_API_KEY` checks to remain dynamic."""

    def __bool__(self):
        return ai_enabled()


OPENAI_API_KEY = _DynamicAIGate()
AI_SETUP_ERROR = "请先在设置页面配置 Claude API Key（支持 .env.local / CLAUDE_CODE_API_KEY / ANTHROPIC_API_KEY）"
PROJECT_ROOT = Path(__file__).resolve().parent
EXIF_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "add_exif.py"
SUPPORTED_IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp")


@st.cache_data(show_spinner=False)
def go_to_page(page_name: str):
    """Switch sidebar page programmatically."""
    st.session_state["requested_page"] = page_name
    st.rerun()


def render_ai_mode_notice(current_page: str):
    """Show a clear onboarding notice when AI is not configured."""
    if ai_enabled() or current_page == "⚙️ 设置":
        return

    st.info(
        "当前处于离线运营模式：你仍可使用今日执行、数据录入、发后追踪、策略和仪表盘。"
        "到「⚙️ 设置 → 🔑 API配置」填写 Claude API Key 后，可解锁 AI 内容生成、合规自查、账号诊断等能力。"
    )


# ==================== 侧边栏 ====================
def render_sidebar():
    with st.sidebar:
        st.markdown("## 🎨 游戏IP真人化·童年角色短视频")
        st.markdown(f"<small style='color:#888'>{ACCOUNT_DESC}</small>", unsafe_allow_html=True)
        st.markdown("---")

        menu_options = [
            "── 🔧 运营工作流 ──",
            "🌅 晨间工作台",
            "📌 今日执行",
            "⏱️ 发后跟踪器",
            "💬 互动任务站",
        ]

        if ai_enabled():
            menu_options.extend([
                "🏥 账号体检",
                "📈 后链路分析",
                "🛡️ 合规自查",
            ])

        menu_options.extend([
            "📚 经验宝库",
        ])

        if ai_enabled():
            menu_options.extend([
                "⚡ 热点快反",
            ])

        menu_options.extend([
            "── 📦 内容与数据 ──",
            "📊 数据复盘",
            "🏠 运营仪表盘",
            "💡 选题灵感库",
            "🖼️ EXIF处理",
        ])

        if ai_enabled():
            menu_options.extend([
                "✍️ AI内容生成",
            ])

        menu_options.extend([
            "📅 发布计划",
            "🎯 涨粉策略",
        ])

        if ai_enabled():
            menu_options.extend([
                "🔥 爆款实验室",
                "💬 评论引流",
            ])

        menu_options.extend([
            "🏆 竞品雷达",
            "📝 笔记管理",
            "⚙️ 设置",
        ])

        default_page = "🌅 晨间工作台"
        pending_page = st.session_state.pop("requested_page", None)
        if pending_page in menu_options:
            st.session_state["sidebar_page"] = pending_page
        elif st.session_state.get("sidebar_page") not in menu_options:
            st.session_state["sidebar_page"] = default_page

        page = st.radio(
            "📋 功能菜单",
            menu_options,
            label_visibility="collapsed",
            key="sidebar_page",
        )

        st.markdown("---")

        # 快速信息
        account = get_account_info()
        if account:
            st.markdown(f"**🎨 账号：** {account.get('nickname', '未设置')}")
            st.markdown(f"**🖼️ 领域：** {account.get('category', ACCOUNT_NICHE)}")
            st.markdown(f"**👥 粉丝：** {account.get('followers', 0):,}")
            adaptive = get_adaptive_tool_profile()
            primary_type = (adaptive.get("content_focus") or {}).get("primary_type")
            if primary_type:
                st.caption(f"本周主推：{primary_type}")
        else:
            st.info("请先在设置中配置账号信息")

        ai_status = "🟢 AI 已启用" if ai_enabled() else "🟠 AI 未启用"
        st.markdown(f"**🤖 状态：** {ai_status}")
        if not ai_enabled():
            st.caption("先用排期/追踪/策略功能也可以，完整 AI 能力请在设置页启用。")
            if st.button("⚙️ 去配置 API", use_container_width=True, key="goto_settings_sidebar"):
                go_to_page("⚙️ 设置")

        st.markdown("---")
        st.caption("🎨 游戏IP真人化 × 童年角色短视频 运营助手")
        st.caption(f"📅 {datetime.datetime.now().strftime('%Y年%m月%d日')}")

        return page


# ==================== 页面：今日执行 ====================

# ==================== Page modules ====================
from pages.page_daily import render_daily, render_morning_patrol
from pages.page_review import render_review
from pages.page_dashboard import render_dashboard
from pages.page_content import render_topic_ideas, render_content_generator
from pages.page_tools import render_exif_tool, render_schedule, render_strategy
from pages.page_engagement import render_engagement_patrol, render_engagement, render_post_tracking
from pages.page_lab import render_viral_lab, render_account_health, render_funnel_analysis, render_compliance
from pages.page_management import render_post_manager, render_competitor
from pages.page_settings import render_settings
from pages.page_extras import render_experience_vault, render_hot_topic

def main():
    try:
        get_adaptive_tool_profile()
    except Exception:
        pass  # adaptive profile warm-up; non-critical
    page = render_sidebar()
    render_ai_mode_notice(page)

    # 运营工作流
    if page == "🌅 晨间工作台":
        render_morning_patrol()
    elif page == "📌 今日执行":
        render_daily()
    elif page == "⏱️ 发后跟踪器":
        render_post_tracking()
    elif page == "💬 互动任务站":
        render_engagement_patrol()
    elif page == "🏥 账号体检":
        render_account_health()
    elif page == "📈 后链路分析":
        render_funnel_analysis()
    elif page == "🛡️ 合规自查":
        render_compliance()
    elif page == "📚 经验宝库":
        render_experience_vault()
    elif page == "⚡ 热点快反":
        render_hot_topic()
    # 内容与数据
    elif page == "📊 数据复盘":
        render_review()
    elif page == "🏠 运营仪表盘":
        render_dashboard()
    elif page == "💡 选题灵感库":
        render_topic_ideas()
    elif page == "🖼️ EXIF处理":
        render_exif_tool()
    elif page == "✍️ AI内容生成":
        render_content_generator()
    elif page == "📅 发布计划":
        render_schedule()
    elif page == "🎯 涨粉策略":
        render_strategy()
    elif page == "🔥 爆款实验室":
        render_viral_lab()
    elif page == "💬 评论引流":
        render_engagement()
    elif page == "🏆 竞品雷达":
        render_competitor()
    elif page == "📝 笔记管理":
        render_post_manager()
    elif page == "⚙️ 设置":
        render_settings()
    elif page.startswith("──"):
        # 分隔线选项，显示默认页面
        render_morning_patrol()


if __name__ == "__main__":
    main()
