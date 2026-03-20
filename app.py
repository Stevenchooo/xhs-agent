"""
🎨 小红书运营Agent - AI油画·当代艺术 智能运营助手
AI油画创作 × 海外当代画家分享 × 智能内容运营
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
)

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="🎨 AI油画·当代艺术 运营Agent",
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
AI_SETUP_ERROR = "请先在设置页面配置 Claude API Key（支持 CLAUDE_CODE_API_KEY / ANTHROPIC_API_KEY）"
PROJECT_ROOT = Path(__file__).resolve().parent
EXIF_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "add_exif.py"
SUPPORTED_IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp")


@st.cache_data(show_spinner=False)
def load_exif_camera_options():
    """Load camera options from scripts/add_exif.py."""
    if not EXIF_SCRIPT_PATH.exists():
        return [], f"未找到脚本：{EXIF_SCRIPT_PATH}"

    try:
        result = subprocess.run(
            [sys.executable, str(EXIF_SCRIPT_PATH), "--list-cameras"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
        )
    except Exception as exc:
        return [], f"读取设备列表失败：{exc}"

    output = "\n".join(
        part for part in [result.stdout.strip(), result.stderr.strip()] if part
    ).strip()
    if result.returncode != 0:
        return [], output or "读取设备列表失败"

    options = []
    current = None
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        camera_match = re.match(r"\[(\d+)\]\s+(.+?)\s+\((.+?)\)$", line)
        if camera_match:
            if current:
                options.append(current)
            idx, model, make = camera_match.groups()
            current = {
                "value": idx,
                "model": model.strip(),
                "make": make.strip(),
                "lens": "",
            }
            continue

        lens_match = re.match(r"镜头:\s*(.+)$", line)
        if lens_match and current:
            current["lens"] = lens_match.group(1).strip()

    if current:
        options.append(current)

    if not options:
        return [], "未解析到设备列表，请检查脚本输出"
    return options, ""


def resolve_exif_folder(folder_input: str) -> Path:
    """Resolve relative folder path against project root."""
    raw = folder_input.strip()
    folder_path = Path(raw)
    if folder_path.is_absolute():
        return folder_path.resolve()
    return (PROJECT_ROOT / folder_path).resolve()


def count_processable_images(folder_path: Path) -> int:
    """Count image files supported by add_exif.py."""
    return sum(
        1
        for item in folder_path.iterdir()
        if item.is_file() and item.suffix.lower() in SUPPORTED_IMAGE_SUFFIXES
    )


def run_exif_script(folder_path: Path, camera_index: str):
    """Execute add_exif.py and return subprocess result."""
    return subprocess.run(
        [
            sys.executable,
            str(EXIF_SCRIPT_PATH),
            str(folder_path),
            "--camera",
            str(camera_index),
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )


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
        st.markdown("## 🎨 AI油画·当代艺术")
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
        else:
            st.info("请先在设置中配置账号信息")

        ai_status = "🟢 AI 已启用" if ai_enabled() else "🟠 AI 未启用"
        st.markdown(f"**🤖 状态：** {ai_status}")
        if not ai_enabled():
            st.caption("先用排期/追踪/策略功能也可以，完整 AI 能力请在设置页启用。")
            if st.button("⚙️ 去配置 API", use_container_width=True, key="goto_settings_sidebar"):
                go_to_page("⚙️ 设置")

        st.markdown("---")
        st.caption("🎨 AI油画 × 当代艺术 运营助手")
        st.caption(f"📅 {datetime.datetime.now().strftime('%Y年%m月%d日')}")

        return page


# ==================== 页面：今日执行 ====================
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
    if pkg.get("data_driven_note"):
        st.markdown(f"""<div class="tip-card" style="border-left-color:#4CAF50">{pkg['data_driven_note']}</div>""", unsafe_allow_html=True)

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


# ==================== 页面：数据复盘 ====================
def render_review():
    st.markdown("## 📊 数据复盘·策略调整")
    st.markdown("_把创作者中心的数据填进来，我告诉你哪里要调整_")

    tab_input, tab_plan, tab_history = st.tabs(["📊 录入数据", "🗺️ 阶段目标", "📋 历史复盘"])

    with tab_input:
        st.markdown("### 📊 录入本周创作者中心数据")
        st.markdown("_每周日录入一次，对比目标，调整下周内容_")

        col1, col2 = st.columns(2)
        with col1:
            r_date = st.date_input("📅 统计截止日期", key="r_date")
            r_posts = st.number_input("📝 累计已发笔记数", min_value=0, value=0, key="r_posts")
            r_followers = st.number_input("👥 当前粉丝数", min_value=0, value=9, key="r_followers")
            r_followers_gain = st.number_input("📈 本周新增粉丝", min_value=0, value=0, key="r_gain")
        with col2:
            r_views = st.number_input("👀 本周平均浏览量/篇", min_value=0, value=0, key="r_views")
            r_likes = st.number_input("❤️ 本周平均点赞/篇", min_value=0, value=0, key="r_likes")
            r_saves = st.number_input("⭐ 本周平均收藏/篇", min_value=0, value=0, key="r_saves")
            r_comments = st.number_input("💬 本周平均评论/篇", min_value=0, value=0, key="r_comments")

        r_best = st.text_input("🔥 本周数据最好的笔记标题", key="r_best",
                               placeholder="写一下哪篇数据最好")
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

            # 展示评估结果
            st.markdown(f"### 📍 当前阶段：{result['phase']}")

            overall_emoji = "🟢" if result["overall"] == "on_track" else "🔴"
            st.markdown(f"**整体状态：** {overall_emoji} {'正常推进' if result['overall'] == 'on_track' else '需要调整'}")

            # 各指标得分
            st.markdown("### 📊 各指标对比目标")
            for label, score in result["scores"].items():
                status_color = "🟢" if score["status"] in ("达标", "超标") else "🟡" if score["status"] == "偏低" else "🔴"
                st.markdown(f"""
                <div class="plan-card">
                    {status_color} <strong>{label}</strong>：实际 <strong>{score['actual']}</strong> vs 目标 {score['target']}
                    （完成率 {score['ratio']}%·{score['status']}）
                </div>
                """, unsafe_allow_html=True)

            # 调整建议
            if result["adjustments"]:
                st.markdown("### 🔧 具体调整建议")
                for adj in result["adjustments"]:
                    st.markdown(f"""<div class="tip-card">{adj}</div>""", unsafe_allow_html=True)

            # 下一步行动
            st.markdown("### ⚡ 下一步行动")
            for action in result["next_actions"]:
                st.markdown(f"**{action}**")

    with tab_plan:
        st.markdown("### 🗺️ 12周成长计划")
        st.markdown("_从9粉到1000粉的4个阶段，每个阶段的目标和内容配比_")

        account = get_account_info()
        current_followers = account.get("followers", 9) if account else 9
        current_phase = get_current_phase(0, current_followers)

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
            st.info("暂无复盘记录。每周日在「录入数据」Tab中提交一次创作者中心数据。")
        else:
            for review in reversed(reviews):
                with st.expander(f"📊 #{review['review_id']} · {review.get('date', '未知日期')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("粉丝", review.get("followers", 0))
                        st.metric("平均浏览", review.get("avg_views", 0))
                        st.metric("平均点赞", review.get("avg_likes", 0))
                    with col2:
                        st.metric("累计笔记", review.get("total_posts", 0))
                        st.metric("平均收藏", review.get("avg_saves", 0))
                        st.metric("本周涨粉", review.get("followers_gain", 0))
                    if review.get("best_post"):
                        st.markdown(f"🔥 最佳笔记：{review['best_post']}（{review.get('best_type', '')}）")


# ==================== 页面：运营仪表盘 ====================
def render_dashboard():
    st.markdown("""
    <div class="main-header">
        <h1>🎨 AI油画·当代艺术 运营Agent</h1>
        <p>用AI探索油画的无限可能 · 分享全球当代艺术 · 让涨粉变得优雅</p>
    </div>
    """, unsafe_allow_html=True)

    account = get_account_info()
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

    st.markdown("---")

    # 核心受众画像 (基于 3/10 爆款数据)
    st.markdown("### 🎯 核心受众画像")
    st.markdown("""
    <div class="tip-card" style="border-left-color:#e94560;">
        <strong>⚠️ 爆款数据揭秘：</strong> 你的受众不是年轻女生，而是<strong>高净值熟龄男性</strong>！
        内容必须抛弃低幼化表达，转向<strong>「艺术投资」「财富密码」「技术前沿」</strong>等有深度的讨论。
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
def render_topic_ideas():
    st.markdown("## 💡 选题灵感库")
    st.markdown("为你的「AI油画·当代艺术」账号精选的选题灵感，可在本地环境中一键生成内容。")

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
def render_exif_tool():
    st.markdown("## 🖼️ 图片EXIF处理")
    st.markdown(
        "选择设备后点击处理，平台会调用脚本批量写入 EXIF 并清除来源元数据。"
    )
    st.info("建议同一批图片统一使用同一个设备。默认预选最新索尼机型 ILCE-9M3。")

    camera_options, camera_error = load_exif_camera_options()
    if camera_error:
        st.error(f"设备列表加载失败：{camera_error}")
        st.caption("请先安装脚本依赖：`pip install Pillow piexif`")
        return

    existing_dirs = []
    for rel_path in ("xhs_agent/data", "data"):
        candidate = PROJECT_ROOT / rel_path
        if candidate.exists() and candidate.is_dir():
            existing_dirs.append(rel_path)

    if existing_dirs:
        st.caption("检测到图片目录：" + " / ".join(f"`{p}`" for p in existing_dirs))

    default_folder = (
        "xhs_agent/data"
        if "xhs_agent/data" in existing_dirs
        else (existing_dirs[0] if existing_dirs else "data")
    )
    folder_input = st.text_input(
        "📁 图片目录（相对项目根目录，或填写绝对路径）",
        value=default_folder,
        key="exif_target_folder",
    )

    default_camera_index = 0
    for i, option in enumerate(camera_options):
        if option["make"].upper() == "SONY" and option["model"] == "ILCE-9M3":
            default_camera_index = i
            break

    selected_camera = st.selectbox(
        "📷 设备选择",
        options=camera_options,
        index=default_camera_index,
        format_func=lambda opt: (
            f"[{opt['value']}] {opt['model']} ({opt['make']})"
            + (f" · {opt['lens']}" if opt.get("lens") else "")
        ),
        key="exif_camera_choice",
    )

    if st.button("🚀 开始处理", type="primary", use_container_width=True, key="exif_run_btn"):
        if not folder_input.strip():
            st.warning("请填写图片目录")
            return

        folder_path = resolve_exif_folder(folder_input)
        if not folder_path.exists() or not folder_path.is_dir():
            st.error(f"目录不存在：{folder_path}")
            return

        image_count = count_processable_images(folder_path)
        if image_count == 0:
            st.warning(f"目录中未找到支持格式图片：{', '.join(SUPPORTED_IMAGE_SUFFIXES)}")
            return

        with st.spinner(f"正在处理 {image_count} 张图片..."):
            result = run_exif_script(folder_path, selected_camera["value"])

        logs = "\n\n".join(
            part for part in [result.stdout.strip(), result.stderr.strip()] if part
        ).strip() or "（脚本无输出）"

        if result.returncode == 0:
            match = re.search(r"处理完成:\s*成功\s*(\d+)\s*\|\s*失败\s*(\d+)", logs)
            if match:
                success_count, fail_count = match.groups()
                st.success(f"✅ 处理完成：成功 {success_count}，失败 {fail_count}")
            else:
                st.success("✅ 处理完成")
            st.caption(f"目录：`{folder_path}`")
            st.caption(
                f"设备：`{selected_camera['model']} ({selected_camera['make']})` "
                f"[{selected_camera['value']}]"
            )
        else:
            st.error("❌ 处理失败，请查看下方日志")

        with st.expander("📄 脚本执行日志", expanded=result.returncode != 0):
            st.code(logs, language="text")


# ==================== 页面：发布计划 ====================
def render_schedule():
    st.markdown("## 📅 一周发布计划")
    st.markdown("为你的AI油画·当代艺术账号量身定制的内容日历")

    account = get_account_info()
    category = account.get("category", ACCOUNT_NICHE) if account else ACCOUNT_NICHE
    followers = account.get("followers", 0) if account else 0

    if not account:
        st.warning("请先在设置页面配置账号信息，以获取个性化的发布计划")
        category = st.selectbox("选择内容领域", CONTENT_CATEGORIES)
        followers = st.number_input("当前粉丝数", min_value=0, value=0)

    plan = get_weekly_plan(category, followers)

    for day in plan:
        with st.expander(f"📆 {day['day']} ({day['date']})", expanded=True):
            if day["posts"]:
                st.markdown("#### 🖼️ 发布计划")
                for i, post in enumerate(day["posts"], 1):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"""
                        <div style="text-align:center">
                            <span class="time-badge">⏰ {post['time']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        hint = post.get("topic_hint", "")
                        st.markdown(f"""
                        **类型：** {post['content_type']} | **分类：** {post['category']}
                        **时间原因：** {post['time_reason']}
                        **内容结构：** {post['type_info']['structure']}
                        **💡 选题提示：** _{hint}_
                        """)
            else:
                st.markdown("_今天可以休息，专注于互动和素材收集_ 🎨")

            st.markdown("#### ✅ 每日任务")
            for task in day["daily_tasks"]:
                st.markdown(f"- {task}")


# ==================== 页面：数据分析 ====================
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
def render_strategy():
    st.markdown("## 🎯 涨粉策略·完整落地手册")
    st.markdown("_不讲套话。每一条都能直接执行。_")

    account = get_account_info()
    followers = account.get("followers", 0) if account else 0
    current = get_current_stage(followers)

    tab_stage, tab_coldstart, tab_sop, tab_artists, tab_engage, tab_money = st.tabs([
        "📍 当前行动",
        "🚀 30天冷启动",
        "📋 内容生产SOP",
        "🎨 画家素材库",
        "📈 互动率提升",
        "💰 变现路径",
    ])

    # ==================== Tab 1: 当前阶段 ====================
    with tab_stage:
        st.markdown(f"""
        <div class="tip-card">
            <strong>📍 你当前在：{current['stage']}（{current['followers']}粉）</strong> · 预估突破周期：{current['duration']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎯 这个阶段只做这几件事")
        for f in current["focus"]:
            st.markdown(f"**→** {f}")

        st.markdown("---")
        st.markdown("### 📋 逐条落地")
        for i, tip in enumerate(current["tips"], 1):
            st.markdown(f"""<div class="tip-card"><strong>行动{i}</strong><br>{tip}</div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📍 其他阶段参考")
        from xhs_agent.config import GROWTH_STAGES
        for stage_name, info in GROWTH_STAGES.items():
            if stage_name == current["stage"]:
                continue
            with st.expander(f"📌 {stage_name}（{info['followers']}粉）"):
                for f in info["focus"]:
                    st.markdown(f"→ {f}")
                for tip in info["tips"][:3]:
                    st.markdown(f"- {tip}")
                if len(info["tips"]) > 3:
                    st.caption(f"...还有{len(info['tips'])-3}条，进入该阶段后查看")

    # ==================== Tab 2: 30天冷启动 ====================
    with tab_coldstart:
        st.markdown("### 🚀 30天冷启动·逐日行动清单")
        from xhs_agent.config import COLD_START_PLAN
        for week in COLD_START_PLAN:
            with st.expander(f"📆 {week['week']}｜目标：{week['goal']}", expanded=True):
                for action in week["actions"]:
                    st.markdown(f"""<div class="tip-card">{action}</div>""", unsafe_allow_html=True)

    # ==================== Tab 3: 内容生产SOP ====================
    with tab_sop:
        st.markdown("### 📋 每种笔记的生产SOP")
        st.markdown("_照着步骤做，不用每次从零想_")

        for sop_name, sop in CONTENT_SOP.items():
            with st.expander(f"📝 {sop_name}｜耗时{sop['耗时']}｜爆款概率{sop['爆款概率']}", expanded=False):
                for j, step in enumerate(sop["步骤"], 1):
                    st.markdown(f"""<div class="tip-card"><strong>Step {j}</strong>：{step}</div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📐 标题公式（直接套）")
        formulas = get_title_formulas()
        cols = st.columns(2)
        for i, f in enumerate(formulas):
            with cols[i % 2]:
                st.markdown(f"""<div class="plan-card"><strong>🔸 {f['formula']}</strong><br>
                <span style="color:#533483">示例：{f['example']}</span><br>
                <small style="color:#888">适用：{f['适用']}</small></div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🖼️ 封面3条规则")
        for title, desc in [
            ("画作占80%", "画本身就是最好的封面，不要加太多装饰。高清是底线"),
            ("标题字要大", "粗体标题放底部/顶部，手机缩略图也能看清。用Canva的中文标题模板"),
            ("统一模板", "选1个模板固定用。颜色/字体/排版一致=品牌感"),
        ]:
            st.markdown(f"**{title}**：{desc}")

        st.markdown("---")
        st.markdown("### 🏷️ 标签直接抄")
        st.code("""# 每篇必带
#油画 #当代艺术 #AI绘画 #艺术 #画家

# AI创作类加
#AI油画 #Midjourney #AI艺术 #提示词分享

# 画家介绍类加
#艺术科普 #画家推荐 #西方油画 + #画家英文名

# 教程类加
#AI绘画教程 #Midjourney教程 #保姆级教程

# 合集类加
#艺术合集 #油画推荐 #值得收藏""", language=None)

    # ==================== Tab 4: 画家素材库 ====================
    with tab_artists:
        st.markdown("### 🎨 画家素材库")
        st.markdown("_10位精选画家，按爆款潜力排序，每位都给了具体的切入角度和AI关键词_")

        for artist in ARTIST_DATABASE:
            with st.expander(
                f"{artist['viral_score']} {artist['name']} ({artist['name_cn']}) · {artist['country']}",
                expanded=False
            ):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"**出生：** {artist['born']}年")
                    st.markdown(f"**风格：** {artist['style']}")
                    st.markdown(f"**制作难度：** {artist['difficulty']}")
                    st.markdown(f"**搜索热度：** {artist['search_volume']}")
                with col2:
                    st.markdown(f"**一句话钩子：** {artist['hook']}")
                    st.markdown(f"**最佳切入角度：** {artist['best_angle']}")

                st.markdown("**AI模仿关键词（可直接用在Prompt里）：**")
                st.code(artist['ai_keywords'], language=None)

    # ==================== Tab 5: 互动率提升 ====================
    with tab_engage:
        st.markdown("### 📈 互动率提升·操作手册")
        st.markdown("_每个指标怎么提，具体做什么，不说废话_")

        for metric_name, tactic in ENGAGEMENT_TACTICS.items():
            with st.expander(f"📊 {metric_name}（目标：{tactic['目标']}）", expanded=True):
                st.markdown(f"**核心逻辑：** {tactic['核心逻辑']}")
                st.markdown("**具体动作：**")
                for action in tactic["具体动作"]:
                    st.markdown(f"""<div class="tip-card">{action}</div>""", unsafe_allow_html=True)

    # ==================== Tab 6: 变现路径 ====================
    with tab_money:
        st.markdown("### 💰 变现路径·时间线")
        st.markdown("_从0到赚钱，每个阶段做什么、能赚多少_")

        for i, milestone in enumerate(MONETIZATION_ROADMAP):
            st.markdown(f"""
            <div class="plan-card">
                <strong>🏁 里程碑：{milestone['milestone']}</strong><br>
                <strong>→ 动作：</strong>{milestone['action']}<br>
                <strong>→ 具体怎么做：</strong>{milestone['detail']}<br>
                <strong>→ 预估收入：</strong>{milestone['revenue']}
            </div>
            """, unsafe_allow_html=True)


# ==================== 页面：笔记管理 ====================
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
        if not posts:
            st.info("暂无笔记记录，请先添加笔记")
        else:
            st.markdown(f"共 **{len(posts)}** 条笔记记录")

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
    <div style="text-align:center; padding:2rem; background:linear-gradient(135deg, #f8f5ff 0%, #fff 100%); border-radius:16px; border:2px solid {score_color}; margin-bottom:1.5rem;">
        <h1 style="font-size:4rem; color:{score_color}; margin:0;">{score}</h1>
        <p style="font-size:1.5rem; color:#333; margin:0.5rem 0;">{level}</p>
        <p style="color:#888; font-size:0.9rem;">账号综合健康度</p>
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
                        st.session_state["hot_desc"] = f"今天是{event['name']}，想从「{event.get('art_angle', '')}」角度出一篇和AI油画·当代艺术结合的笔记"
                        st.info("请切换到「⚡ 快速出内容」Tab，热点描述已自动填入")
        else:
            st.info("未来14天没有预设的热点节日。但你可以自己发现热点并在「⚡ 快速出内容」中使用！")


# ==================== 页面：设置 ====================
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
            index=CONTENT_CATEGORIES.index(account.get("category", "AI油画创作"))
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
                           placeholder="例如：🎨 AI油画探索者 | 分享海外当代画家的精彩世界 | 用科技与艺术碰撞美的火花",
                           key="s_bio")
        target = st.text_input(
            "运营目标",
            value=account.get("target", ""),
            placeholder="例如：3个月涨粉5000，成为AI油画领域头部账号",
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
        2. 设置环境变量：`CLAUDE_CODE_API_KEY` 或 `ANTHROPIC_API_KEY`
        3. 如需代理/中转，可额外设置：`CLAUDE_BASE_URL` / `ANTHROPIC_BASE_URL` / `CLAUDE_MODEL`
        """)
        st.caption("默认模型已设为 `claude-sonnet-4-6`，更适合这类日常运营生成场景。")

        new_key = st.text_input("Claude API Key", value=cfg.CLAUDE_API_KEY, type="password", key="s_api_key")
        new_url = st.text_input("Claude Base URL", value=cfg.CLAUDE_BASE_URL, key="s_api_url")
        new_model = st.text_input("模型名称", value=cfg.CLAUDE_MODEL, key="s_model")

        if st.button("💾 保存API配置", type="primary", key="s_api_save"):
            import xhs_agent.content as content_mod

            cfg.set_ai_runtime_config(new_key, new_url, new_model)
            content_mod.OPENAI_MODEL = cfg.CLAUDE_MODEL
            st.success("✅ Claude API 配置已保存（本次会话有效）！")
            st.rerun()


# ==================== 主程序 ====================
def main():
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
