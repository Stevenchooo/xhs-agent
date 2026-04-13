# Latest Metrics Sync And History Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a lightweight SQLite-backed metrics history store while keeping the current JSON files as compatibility writes for weekly review data and operations snapshots.

**Architecture:** Introduce a focused `metrics_store` module that owns schema creation, dual-write persistence, and change diff generation. Keep `review.py` and `tracker.py` as the current write entry points, then expose the new data through small additions to `app.py` rather than replacing existing dashboard logic.

**Tech Stack:** Python stdlib, sqlite3, Streamlit, unittest

---

### Task 1: Add the failing persistence tests

**Files:**
- Modify: `tests/test_ops_snapshot_pipeline.py`
- Create: `xhs_agent/metrics_store.py`
- Modify: `xhs_agent/config.py`

- [ ] **Step 1: Write the failing tests**

Add tests that express these expected behaviors:

```python
def test_save_review_syncs_latest_account_and_records_changes(self):
    review.save_review({
        "date": "2026-04-01",
        "total_posts": 12,
        "followers": 120,
        "followers_gain": 8,
        "avg_views": 820,
        "avg_likes": 28,
        "avg_saves": 9,
        "avg_comments": 3,
        "best_post": "A",
        "best_type": "游戏IP真人化",
        "best_post_views": 2400,
    })
    review.save_review({
        "date": "2026-04-08",
        "total_posts": 14,
        "followers": 138,
        "followers_gain": 18,
        "avg_views": 1060,
        "avg_likes": 35,
        "avg_saves": 12,
        "avg_comments": 4,
        "best_post": "B",
        "best_type": "游戏热点快反",
        "best_post_views": 3800,
    })
    latest_account = tracker.get_account_info()
    changes = tracker.get_recent_metric_changes(limit=10, source_type="weekly_review")
    self.assertEqual(latest_account["followers"], 138)
    self.assertTrue(any(c["metric_key"] == "followers" for c in changes))
```

```python
def test_operations_snapshot_records_recent_changes(self):
    tracker.save_operations_snapshot(self._sample_snapshot())
    tracker.save_operations_snapshot({
        **self._sample_snapshot(),
        "metrics": {**self._sample_snapshot()["metrics"], "views": 36000},
    })
    changes = tracker.get_recent_metric_changes(limit=10, source_type="operations_snapshot")
    self.assertTrue(any(c["metric_key"] == "views" for c in changes))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`

Expected: FAIL because SQLite-backed history helpers and recent-change readers do not exist yet.

- [ ] **Step 3: Write minimal implementation**

Create the config path and SQLite schema module:

```python
# xhs_agent/config.py
METRICS_DB_FILE = os.path.join(DATA_DIR, "metrics.sqlite3")
```

```python
# xhs_agent/metrics_store.py
def record_weekly_review(review_data: dict) -> dict: ...
def record_operations_snapshot(snapshot: dict) -> dict: ...
def get_recent_metric_changes(limit: int = 20, source_type: str | None = None) -> list[dict]: ...
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`

Expected: PASS for the new persistence/history expectations.

### Task 2: Wire weekly review into system latest data

**Files:**
- Modify: `xhs_agent/review.py`
- Modify: `xhs_agent/tracker.py`
- Modify: `tests/test_ops_snapshot_pipeline.py`

- [ ] **Step 1: Write the failing test**

Assert that calling `save_review()` updates the system’s latest review snapshot and current follower count:

```python
latest_review = tracker.get_latest_review_snapshot()
self.assertEqual(latest_review["avg_views"], 1060)
self.assertEqual(tracker.get_account_info()["followers"], 138)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`

Expected: FAIL because `save_review()` currently only writes `reviews.json`.

- [ ] **Step 3: Write minimal implementation**

Add a tracker helper that updates `analytics.json` and delegates to the SQLite store:

```python
def sync_latest_review_snapshot(review_data: dict) -> dict:
    data = _load_json(ANALYTICS_FILE)
    account_info = data.get("account_info", {})
    account_info["followers"] = int(review_data.get("followers", 0) or 0)
    account_info["updated_at"] = datetime.datetime.now().isoformat()
    data["account_info"] = account_info
    data["latest_review_snapshot"] = {
        **review_data,
        "recorded_at": datetime.datetime.now().isoformat(),
    }
    _save_json(ANALYTICS_FILE, data)
    return metrics_store.record_weekly_review(review_data)
```

Then call it from `review.save_review()` after appending to `reviews.json`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`

Expected: PASS with latest review sync working.

### Task 3: Extend operations snapshot write path

**Files:**
- Modify: `xhs_agent/tracker.py`
- Modify: `tests/test_ops_snapshot_pipeline.py`

- [ ] **Step 1: Write the failing test**

Assert that `save_operations_snapshot()` still writes JSON latest state and now also produces change history rows:

```python
latest = tracker.get_latest_operations_snapshot()
changes = tracker.get_recent_metric_changes(limit=10, source_type="operations_snapshot")
self.assertEqual(latest["metrics"]["views"], 36000)
self.assertTrue(any(c["metric_key"] == "views" for c in changes))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`

Expected: FAIL because the current snapshot path does not populate the SQLite change log.

- [ ] **Step 3: Write minimal implementation**

Update the existing save helper to dual-write:

```python
def save_operations_snapshot(snapshot: dict) -> dict:
    ...
    _save_json(OPERATIONS_SNAPSHOT_FILE, data)
    metrics_store.record_operations_snapshot(enriched)
    return enriched
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`

Expected: PASS with JSON compatibility preserved.

### Task 4: Add the UI entry points

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Write the failing test or verification target**

There is no focused Streamlit test harness in this repo, so define the manual verification target before editing:

```text
Review page shows:
1. a weekly review form that still works
2. a new operations snapshot form
3. a recent metric changes section
4. a latest weekly review summary block
```

- [ ] **Step 2: Implement the minimal UI changes**

Update imports and add UI blocks:

```python
from xhs_agent.tracker import (
    ...,
    save_operations_snapshot,
    get_recent_metric_changes,
    get_latest_review_snapshot,
)
```

```python
latest_review = get_latest_review_snapshot()
changes = get_recent_metric_changes(limit=20)
```

Add:
- a new `📈 运营面板快照` tab with a save button
- a new `🕓 数据变化` tab listing recent changes
- a small latest-review summary card in dashboard or review flow

- [ ] **Step 3: Run targeted verification**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`

Expected: PASS

### Task 5: Final verification

**Files:**
- Modify: changed files only if verification reveals issues

- [ ] **Step 1: Run the targeted unit tests**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`

- [ ] **Step 2: Check lints on changed files**

Use Cursor lints on:
- `app.py`
- `xhs_agent/config.py`
- `xhs_agent/metrics_store.py`
- `xhs_agent/review.py`
- `xhs_agent/tracker.py`
- `tests/test_ops_snapshot_pipeline.py`

- [ ] **Step 3: Sanity-check the requirements**

Confirm all of these are true:
- weekly review writes JSON and SQLite
- weekly review updates latest follower count in system data
- operations snapshot writes JSON and SQLite
- recent metric changes can be queried and displayed
- no existing snapshot-based daily summary behavior regressed
