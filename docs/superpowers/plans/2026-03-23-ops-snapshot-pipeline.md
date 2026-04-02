# Ops Snapshot Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a persistent operations-snapshot pipeline so latest dashboard metrics can feed today's summary and execution focus even when historical tracker data is incomplete.

**Architecture:** Add a dedicated operations snapshot store in `xhs_agent/tracker.py`, seed it with the current dashboard snapshot, and update `xhs_agent/strategy.py` to merge latest operations insight with historical tracker advice. Surface the merged result through the existing daily package flow and dashboard rendering.

**Tech Stack:** Python stdlib, Streamlit, unittest

---

### Task 1: Snapshot storage and tests

**Files:**
- Create: `tests/test_ops_snapshot_pipeline.py`
- Modify: `xhs_agent/config.py`
- Modify: `xhs_agent/tracker.py`

- [ ] **Step 1: Write the failing tests**

Test snapshot persistence and latest-snapshot retrieval with an isolated temp data directory.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`
Expected: FAIL because snapshot helpers do not exist yet.

- [ ] **Step 3: Write minimal implementation**

Add an operations snapshot file constant plus save/load/latest helper functions.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`
Expected: PASS

### Task 2: Strategy integration and tests

**Files:**
- Modify: `tests/test_ops_snapshot_pipeline.py`
- Modify: `xhs_agent/strategy.py`

- [ ] **Step 1: Write the failing tests**

Test that a latest operations snapshot can produce summary text, tool focus, and execution focus even when historical tracker stats are unavailable.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`
Expected: FAIL because strategy does not consume snapshot data yet.

- [ ] **Step 3: Write minimal implementation**

Add snapshot-aware execution-brief generation and merge behavior with historical tracker advice.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`
Expected: PASS

### Task 3: Seed current snapshot and expose summary

**Files:**
- Modify: `app.py`
- Create: `xhs_agent/data/operations_snapshot.json`

- [ ] **Step 1: Write the failing test**

Extend tests to cover that latest snapshot insight is exposed through today's package fields.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`
Expected: FAIL until the package flow exposes snapshot-derived content.

- [ ] **Step 3: Write minimal implementation**

Seed today's snapshot from the provided dashboard data and render an operations summary block in the daily view.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`
Expected: PASS

### Task 4: Verification

**Files:**
- Modify: `tests/test_ops_snapshot_pipeline.py` if needed

- [ ] **Step 1: Run targeted verification**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`

- [ ] **Step 2: Run lints for changed files**

Use Cursor lints on `app.py`, `xhs_agent/config.py`, `xhs_agent/tracker.py`, `xhs_agent/strategy.py`, `tests/test_ops_snapshot_pipeline.py`

- [ ] **Step 3: Review final behavior**

Confirm today's package includes:
- snapshot-based operations summary
- snapshot-driven tool priorities
- snapshot-driven execution focus
