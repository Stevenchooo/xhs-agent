import os
import tempfile
import unittest
import gc
import warnings

from xhs_agent import metrics_store
from xhs_agent import review, tracker


class MetricsHistoryPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.original_tracker_paths = {
            "DATA_DIR": tracker.DATA_DIR,
            "ANALYTICS_FILE": tracker.ANALYTICS_FILE,
            "CONTENT_HISTORY_FILE": tracker.CONTENT_HISTORY_FILE,
            "POST_TRACKING_FILE": tracker.POST_TRACKING_FILE,
            "ENGAGEMENT_LOG_FILE": tracker.ENGAGEMENT_LOG_FILE,
            "OPERATIONS_SNAPSHOT_FILE": tracker.OPERATIONS_SNAPSHOT_FILE,
        }
        self.original_review_paths = {
            "DATA_DIR": review.DATA_DIR,
            "REVIEW_FILE": review.REVIEW_FILE,
        }

        tracker.DATA_DIR = self.temp_dir.name
        tracker.ANALYTICS_FILE = os.path.join(self.temp_dir.name, "analytics.json")
        tracker.CONTENT_HISTORY_FILE = os.path.join(self.temp_dir.name, "content_history.json")
        tracker.POST_TRACKING_FILE = os.path.join(self.temp_dir.name, "post_tracking.json")
        tracker.ENGAGEMENT_LOG_FILE = os.path.join(self.temp_dir.name, "engagement_log.json")
        tracker.OPERATIONS_SNAPSHOT_FILE = os.path.join(self.temp_dir.name, "operations_snapshot.json")
        review.DATA_DIR = self.temp_dir.name
        review.REVIEW_FILE = os.path.join(self.temp_dir.name, "reviews.json")
        self.original_metrics_db_file = metrics_store.METRICS_DB_FILE
        metrics_store.METRICS_DB_FILE = os.path.join(self.temp_dir.name, "metrics.sqlite3")

        self.addCleanup(self._restore_tracker_paths)
        self.addCleanup(self._restore_review_paths)
        self.addCleanup(self._restore_metrics_store_path)

    def _restore_tracker_paths(self):
        for key, value in self.original_tracker_paths.items():
            setattr(tracker, key, value)

    def _restore_review_paths(self):
        for key, value in self.original_review_paths.items():
            setattr(review, key, value)

    def _restore_metrics_store_path(self):
        metrics_store.METRICS_DB_FILE = self.original_metrics_db_file

    def _sample_snapshot(self):
        return {
            "period": {"start": "04-01", "end": "04-08"},
            "metrics": {
                "views": 32000,
                "viewer_followers": 3751,
                "avg_watch_seconds": 20,
                "total_watch_hours": 26.8,
                "conversion_rate": 0,
            },
            "traffic_sources": [
                {"name": "首页推荐", "percent": 85},
                {"name": "搜索", "percent": 5},
                {"name": "个人主页", "percent": 2},
                {"name": "其他来源", "percent": 8},
            ],
            "viewer_time": {
                "peak_window": "晚间",
                "peak_hour_label": "24:00附近",
            },
        }

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
        latest_review = tracker.get_latest_review_snapshot()
        changes = tracker.get_recent_metric_changes(limit=10, source_type="weekly_review")

        self.assertEqual(latest_account["followers"], 138)
        self.assertEqual(latest_review["avg_views"], 1060)
        self.assertTrue(any(change["metric_key"] == "followers" for change in changes))

    def test_operations_snapshot_records_recent_changes(self):
        tracker.save_operations_snapshot(self._sample_snapshot())
        tracker.save_operations_snapshot({
            **self._sample_snapshot(),
            "metrics": {
                **self._sample_snapshot()["metrics"],
                "views": 36000,
                "avg_watch_seconds": 26,
            },
            "traffic_sources": [
                {"name": "首页推荐", "percent": 81},
                {"name": "搜索", "percent": 9},
                {"name": "个人主页", "percent": 4},
                {"name": "其他来源", "percent": 6},
            ],
            "viewer_time": {
                "peak_window": "晚间",
                "peak_hour_label": "22:00-23:00",
            },
        })

        latest = tracker.get_latest_operations_snapshot()
        changes = tracker.get_recent_metric_changes(limit=10, source_type="operations_snapshot")

        self.assertEqual(latest["metrics"]["views"], 36000)
        self.assertTrue(any(change["metric_key"] == "views" for change in changes))

    def test_metrics_store_does_not_leave_unclosed_connections(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ResourceWarning)

            review.save_review({
                "date": "2026-04-08",
                "followers": 170,
                "followers_gain": 30,
                "avg_views": 1060,
                "avg_likes": 35,
                "avg_saves": 12,
                "avg_comments": 4,
                "best_post": "B",
                "best_type": "游戏热点快反",
                "best_post_views": 3800,
            })
            tracker.save_operations_snapshot(self._sample_snapshot())
            tracker.get_recent_metric_changes(limit=10)
            tracker.get_latest_review_snapshot()

            gc.collect()

        resource_warnings = [w for w in caught if issubclass(w.category, ResourceWarning)]
        self.assertEqual(resource_warnings, [])


if __name__ == "__main__":
    unittest.main()
