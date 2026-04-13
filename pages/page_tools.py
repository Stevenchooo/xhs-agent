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
from pages.shared_runtime import PROJECT_ROOT, EXIF_SCRIPT_PATH, SUPPORTED_IMAGE_SUFFIXES
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
    st.markdown(f"为你的「{ACCOUNT_NICHE}」账号量身定制的内容日历")

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




