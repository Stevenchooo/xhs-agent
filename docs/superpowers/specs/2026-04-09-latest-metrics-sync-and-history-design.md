# Latest Metrics Sync And History Design

## Goal
让系统能稳定接收两类“最新数据”并记录变化历史：

- 周复盘数据：粉丝、平均浏览/点赞/收藏/评论、最佳笔记等
- 运营面板快照：观看数、粉丝观看、来源结构、观看时长、转化率等

同时保持现有 JSON 文件兼容，不一次性推翻当前页面和读取逻辑。

## Current Problems
- `save_review()` 只把周复盘写入 `reviews.json`，不会把最新粉丝和最新周摘要同步到系统主数据。
- `save_operations_snapshot()` 已经能写入 `operations_snapshot.json`，但页面里没有轻量录入入口。
- 系统缺少统一的“变化历史”存储层，无法方便查看某个指标从多少变到多少。
- 现有数据分散在 `analytics.json`、`content_history.json`、`operations_snapshot.json`、`reviews.json`，查询最近变化需要人工比对。

## Design Principles
- 保持兼容：现有 JSON 继续写，避免破坏当前页面。
- 轻量优先：使用 Python 标准库 `sqlite3`，不引入新依赖。
- 改动收束：新增一个独立存储模块，不把业务逻辑塞进 `app.py`。
- 先解决“最新数据”和“变化历史”，不顺手做整库迁移。

## Proposed Architecture

### 1. Add A Lightweight SQLite Store
新增 `xhs_agent/metrics_store.py`，使用 `xhs_agent/data/metrics.sqlite3` 维护 3 张表：

- `weekly_reviews`
  - 存放周复盘录入值和原始 payload
- `operations_snapshots`
  - 存放运营面板快照的关键字段和原始 payload
- `metric_changes`
  - 存放与上一条同类记录相比发生变化的字段
  - 字段包括：`source_type`、`source_record_id`、`metric_key`、`metric_label`、`old_value`、`new_value`、`created_at`

### 2. Keep JSON As The Compatibility Layer
不替换现有 JSON，而是改成“双写”：

- 周复盘提交时：
  - 继续写 `reviews.json`
  - 同步写 SQLite `weekly_reviews`
  - 同步更新 `analytics.json` 里的 `account_info.followers`
  - 同步写入 `latest_review_snapshot`
- 运营面板快照保存时：
  - 继续写 `operations_snapshot.json`
  - 同步写 SQLite `operations_snapshots`
  - 自动生成对应的 `metric_changes`

### 3. Normalize Change Tracking
变化记录只追踪用户最关心且可展示的字段。

周复盘追踪字段：
- `followers`
- `followers_gain`
- `avg_views`
- `avg_likes`
- `avg_saves`
- `avg_comments`
- `best_type`
- `best_post_views`

运营面板追踪字段：
- `views`
- `viewer_followers`
- `avg_watch_seconds`
- `total_watch_hours`
- `conversion_rate`
- `primary_source_name`
- `primary_source_percent`
- `search_percent`
- `homepage_percent`
- `peak_window`
- `peak_hour_label`

### 4. Surface Latest Data In UI
在 `app.py` 中补两类展示：

- `📈 运营面板快照` 录入入口
  - 手动录入统计周期、核心指标、流量来源、流量高峰
- `🕓 数据变化` 展示区
  - 展示最近若干条变化，如 `粉丝数 120 -> 138`

同时在仪表盘或复盘页展示一条轻量“最近周复盘摘要”，让最新录入值真正进入系统视图，而不是只躺在历史 JSON 里。

## File Changes
- Create: `xhs_agent/metrics_store.py`
- Modify: `xhs_agent/config.py`
- Modify: `xhs_agent/tracker.py`
- Modify: `xhs_agent/review.py`
- Modify: `app.py`
- Modify: `tests/test_ops_snapshot_pipeline.py` or add a focused new test file

## Data Flow

### Weekly Review
`app.py review form` -> `review.save_review()` -> `reviews.json` + `tracker.sync_latest_review_snapshot()` -> `analytics.json latest/account_info` + `metrics_store.record_weekly_review()` -> `metric_changes`

### Operations Snapshot
`app.py operations snapshot form` -> `tracker.save_operations_snapshot()` -> `operations_snapshot.json` + `metrics_store.record_operations_snapshot()` -> `metric_changes`

## Risks
- JSON 与 SQLite 双写如果不收口，容易分叉。
- 现有测试主要覆盖快照 JSON 路径，新增 SQLite 后必须补回归测试。
- 页面层不要直接拼接 SQL；所有数据库访问都放进 `metrics_store.py` 或 `tracker.py` 包装函数中。

## Non-Goals
- 不做现有 JSON 数据向 SQLite 的一次性迁移。
- 不把单篇笔记所有指标历史统一迁入 SQLite。
- 不重构现有 dashboard 指标计算逻辑。

## Verification Plan
- 单测覆盖：
  - 周复盘双写和最新账号数据同步
  - 运营面板快照双写
  - 变化记录生成与读取
- 手动验证：
  - 提交周复盘后，侧边栏粉丝数更新
  - 提交运营面板快照后，`今日执行` 读到最新快照
  - `数据变化` 区块能展示最近变化
