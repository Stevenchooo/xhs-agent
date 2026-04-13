"""Lightweight SQLite-backed metric history store."""

import json
import os
import sqlite3
from datetime import datetime
from contextlib import closing
from typing import Any, Dict, List, Optional

from .config import METRICS_DB_FILE


WEEKLY_REVIEW_FIELDS = [
    ("followers", "粉丝数"),
    ("followers_gain", "本周新增粉丝"),
    ("avg_views", "平均浏览"),
    ("avg_likes", "平均点赞"),
    ("avg_saves", "平均收藏"),
    ("avg_comments", "平均评论"),
    ("best_type", "最佳内容类型"),
    ("best_post_views", "最佳笔记浏览"),
]

OPERATIONS_SNAPSHOT_FIELDS = [
    ("views", "观看总数"),
    ("viewer_followers", "观看粉丝"),
    ("avg_watch_seconds", "平均观看时长"),
    ("total_watch_hours", "总观看时长"),
    ("conversion_rate", "转化率"),
    ("primary_source_name", "主要流量来源"),
    ("primary_source_percent", "主要流量来源占比"),
    ("search_percent", "搜索来源占比"),
    ("homepage_percent", "个人主页来源占比"),
    ("peak_window", "流量高峰时段"),
    ("peak_hour_label", "流量高峰标签"),
]


def _now_iso() -> str:
    return datetime.now().isoformat()


def _ensure_db_dir() -> None:
    db_dir = os.path.dirname(METRICS_DB_FILE)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)


def _connect() -> sqlite3.Connection:
    _ensure_db_dir()
    conn = sqlite3.connect(METRICS_DB_FILE)
    conn.row_factory = sqlite3.Row
    _ensure_schema(conn)
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS weekly_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_date TEXT,
            total_posts INTEGER,
            followers INTEGER,
            followers_gain INTEGER,
            avg_views INTEGER,
            avg_likes INTEGER,
            avg_saves INTEGER,
            avg_comments INTEGER,
            best_post TEXT,
            best_type TEXT,
            best_post_views INTEGER,
            payload_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS operations_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            period_start TEXT,
            period_end TEXT,
            views INTEGER,
            viewer_followers INTEGER,
            avg_watch_seconds REAL,
            total_watch_hours REAL,
            conversion_rate REAL,
            primary_source_name TEXT,
            primary_source_percent REAL,
            search_percent REAL,
            homepage_percent REAL,
            other_percent REAL,
            peak_window TEXT,
            peak_hour_label TEXT,
            payload_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS metric_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT NOT NULL,
            source_record_id INTEGER NOT NULL,
            metric_key TEXT NOT NULL,
            metric_label TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_metric_changes_source_created_at
        ON metric_changes (source_type, created_at DESC)
        """
    )
    conn.commit()


def _serialize_payload(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _stringify_value(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def _values_differ(old_value: Any, new_value: Any) -> bool:
    return _stringify_value(old_value) != _stringify_value(new_value)


def _insert_changes(
    conn: sqlite3.Connection,
    source_type: str,
    source_record_id: int,
    fields: List[tuple],
    previous_row: Optional[sqlite3.Row],
    current_record: Dict[str, Any],
    created_at: str,
) -> List[Dict[str, Any]]:
    changes: List[Dict[str, Any]] = []
    if previous_row is None:
        return changes

    for metric_key, metric_label in fields:
        old_value = previous_row[metric_key]
        new_value = current_record.get(metric_key)
        if not _values_differ(old_value, new_value):
            continue
        change = {
            "source_type": source_type,
            "source_record_id": source_record_id,
            "metric_key": metric_key,
            "metric_label": metric_label,
            "old_value": _stringify_value(old_value),
            "new_value": _stringify_value(new_value),
            "created_at": created_at,
        }
        conn.execute(
            """
            INSERT INTO metric_changes (
                source_type, source_record_id, metric_key, metric_label,
                old_value, new_value, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                change["source_type"],
                change["source_record_id"],
                change["metric_key"],
                change["metric_label"],
                change["old_value"],
                change["new_value"],
                change["created_at"],
            ),
        )
        changes.append(change)
    return changes


def _lookup_source_percent(sources: List[Dict[str, Any]], name: str) -> float:
    for item in sources:
        if item.get("name") == name:
            return float(item.get("percent") or 0)
    return 0.0


def _build_weekly_review_record(review_data: Dict[str, Any]) -> Dict[str, Any]:
    created_at = review_data.get("review_date") or review_data.get("recorded_at") or _now_iso()
    return {
        "review_date": review_data.get("date"),
        "total_posts": int(review_data.get("total_posts", 0) or 0),
        "followers": int(review_data.get("followers", 0) or 0),
        "followers_gain": int(review_data.get("followers_gain", 0) or 0),
        "avg_views": int(review_data.get("avg_views", 0) or 0),
        "avg_likes": int(review_data.get("avg_likes", 0) or 0),
        "avg_saves": int(review_data.get("avg_saves", 0) or 0),
        "avg_comments": int(review_data.get("avg_comments", 0) or 0),
        "best_post": review_data.get("best_post", ""),
        "best_type": review_data.get("best_type", ""),
        "best_post_views": int(review_data.get("best_post_views", 0) or 0),
        "payload_json": _serialize_payload(review_data),
        "created_at": created_at,
    }


def _build_operations_snapshot_record(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    period = snapshot.get("period") or {}
    metrics = snapshot.get("metrics") or {}
    sources = snapshot.get("traffic_sources") or []
    viewer_time = snapshot.get("viewer_time") or {}
    primary_source = sources[0] if sources else {}

    return {
        "period_start": period.get("start"),
        "period_end": period.get("end"),
        "views": int(metrics.get("views", 0) or 0),
        "viewer_followers": int(metrics.get("viewer_followers", 0) or 0),
        "avg_watch_seconds": float(metrics.get("avg_watch_seconds", 0) or 0),
        "total_watch_hours": float(metrics.get("total_watch_hours", 0) or 0),
        "conversion_rate": float(metrics.get("conversion_rate", 0) or 0),
        "primary_source_name": primary_source.get("name", ""),
        "primary_source_percent": float(primary_source.get("percent", 0) or 0),
        "search_percent": _lookup_source_percent(sources, "搜索"),
        "homepage_percent": _lookup_source_percent(sources, "个人主页"),
        "other_percent": _lookup_source_percent(sources, "其他来源"),
        "peak_window": viewer_time.get("peak_window", ""),
        "peak_hour_label": viewer_time.get("peak_hour_label", ""),
        "payload_json": _serialize_payload(snapshot),
        "created_at": snapshot.get("recorded_at") or _now_iso(),
    }


def record_weekly_review(review_data: Dict[str, Any]) -> Dict[str, Any]:
    record = _build_weekly_review_record(review_data)
    with closing(_connect()) as conn:
        previous_row = conn.execute(
            "SELECT * FROM weekly_reviews ORDER BY id DESC LIMIT 1"
        ).fetchone()
        cursor = conn.execute(
            """
            INSERT INTO weekly_reviews (
                review_date, total_posts, followers, followers_gain,
                avg_views, avg_likes, avg_saves, avg_comments,
                best_post, best_type, best_post_views,
                payload_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["review_date"],
                record["total_posts"],
                record["followers"],
                record["followers_gain"],
                record["avg_views"],
                record["avg_likes"],
                record["avg_saves"],
                record["avg_comments"],
                record["best_post"],
                record["best_type"],
                record["best_post_views"],
                record["payload_json"],
                record["created_at"],
            ),
        )
        changes = _insert_changes(
            conn=conn,
            source_type="weekly_review",
            source_record_id=cursor.lastrowid,
            fields=WEEKLY_REVIEW_FIELDS,
            previous_row=previous_row,
            current_record=record,
            created_at=record["created_at"],
        )
        conn.commit()
    return {"id": cursor.lastrowid, "changes": changes}


def record_operations_snapshot(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    record = _build_operations_snapshot_record(snapshot)
    with closing(_connect()) as conn:
        previous_row = conn.execute(
            "SELECT * FROM operations_snapshots ORDER BY id DESC LIMIT 1"
        ).fetchone()
        cursor = conn.execute(
            """
            INSERT INTO operations_snapshots (
                period_start, period_end, views, viewer_followers,
                avg_watch_seconds, total_watch_hours, conversion_rate,
                primary_source_name, primary_source_percent,
                search_percent, homepage_percent, other_percent,
                peak_window, peak_hour_label, payload_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["period_start"],
                record["period_end"],
                record["views"],
                record["viewer_followers"],
                record["avg_watch_seconds"],
                record["total_watch_hours"],
                record["conversion_rate"],
                record["primary_source_name"],
                record["primary_source_percent"],
                record["search_percent"],
                record["homepage_percent"],
                record["other_percent"],
                record["peak_window"],
                record["peak_hour_label"],
                record["payload_json"],
                record["created_at"],
            ),
        )
        changes = _insert_changes(
            conn=conn,
            source_type="operations_snapshot",
            source_record_id=cursor.lastrowid,
            fields=OPERATIONS_SNAPSHOT_FIELDS,
            previous_row=previous_row,
            current_record=record,
            created_at=record["created_at"],
        )
        conn.commit()
    return {"id": cursor.lastrowid, "changes": changes}


def get_latest_weekly_review() -> Dict[str, Any]:
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT payload_json FROM weekly_reviews ORDER BY id DESC LIMIT 1"
        ).fetchone()
    if not row:
        return {}
    return json.loads(row["payload_json"])


def get_recent_metric_changes(limit: int = 20, source_type: Optional[str] = None) -> List[Dict[str, Any]]:
    limit = max(int(limit or 20), 1)
    sql = """
        SELECT source_type, source_record_id, metric_key, metric_label,
               old_value, new_value, created_at
        FROM metric_changes
    """
    params: List[Any] = []
    if source_type:
        sql += " WHERE source_type = ?"
        params.append(source_type)
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    with closing(_connect()) as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(row) for row in rows]
