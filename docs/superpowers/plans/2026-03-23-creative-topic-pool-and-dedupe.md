# Creative Topic Pool And Dedupe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add precise topic-level dedupe and a higher-imagination creative topic pool so daily recommendations avoid repeats and prefer fresher ideas.

**Architecture:** Keep the existing verified `DAILY_PACKAGES` as a fallback pool, add a new creative-first package pool with explicit `topic_id` metadata, and update daily selection to dedupe by `topic_id`, aliases, and legacy fuzzy matching. Extend tests so topic-id dedupe and creative-pool priority are both locked in.

**Tech Stack:** Python stdlib, unittest

---

### Task 1: Add failing tests for stronger selection rules

**Files:**
- Modify: `tests/test_ops_snapshot_pipeline.py`
- Modify: `xhs_agent/daily.py`

- [ ] **Step 1: Write the failing test**

Add one test proving a published `topic_id` blocks a package even if the title differs, and one test proving the creative pool is preferred when its topic is still unpublished.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`
Expected: FAIL because current selection does not support topic-id dedupe or creative-pool priority.

- [ ] **Step 3: Write minimal implementation**

Add selection helpers and package metadata only needed to make the tests pass.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`
Expected: PASS

### Task 2: Add creative-first package pool

**Files:**
- Modify: `xhs_agent/daily.py`

- [ ] **Step 1: Define the new pool**

Add a focused set of creative-first packages with explicit `topic_id`, dedupe aliases, and more imaginative themes.

- [ ] **Step 2: Route daily selection through the new pool first**

Keep existing weekday logic as fallback, but try creative candidates first.

- [ ] **Step 3: Keep weekly output stable**

Make weekly packages also avoid already-published topics while still producing deterministic output.

- [ ] **Step 4: Re-run tests**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`
Expected: PASS

### Task 3: Verification

**Files:**
- Modify: `xhs_agent/daily.py` if needed

- [ ] **Step 1: Run targeted verification**

Run: `python3 -m unittest tests.test_ops_snapshot_pipeline -v`

- [ ] **Step 2: Run real output check**

Run: `python3 scripts/daily_brief.py`
Expected: today’s package is unpublished and comes from the creative-first path when available.

- [ ] **Step 3: Run lints**

Check `xhs_agent/daily.py` and `tests/test_ops_snapshot_pipeline.py`
