import os
import tempfile
import unittest
import datetime
from unittest import mock

from xhs_agent import daily, strategy, tracker
from xhs_agent import metrics_store


class OpsSnapshotPipelineTests(unittest.TestCase):
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
        self.original_metrics_db_file = metrics_store.METRICS_DB_FILE

        tracker.DATA_DIR = self.temp_dir.name
        tracker.ANALYTICS_FILE = os.path.join(self.temp_dir.name, "analytics.json")
        tracker.CONTENT_HISTORY_FILE = os.path.join(self.temp_dir.name, "content_history.json")
        tracker.POST_TRACKING_FILE = os.path.join(self.temp_dir.name, "post_tracking.json")
        tracker.ENGAGEMENT_LOG_FILE = os.path.join(self.temp_dir.name, "engagement_log.json")
        tracker.OPERATIONS_SNAPSHOT_FILE = os.path.join(self.temp_dir.name, "operations_snapshot.json")
        metrics_store.METRICS_DB_FILE = os.path.join(self.temp_dir.name, "metrics.sqlite3")

        self.addCleanup(self._restore_tracker_paths)
        self.addCleanup(self._restore_metrics_store_path)

    def _restore_tracker_paths(self):
        for key, value in self.original_tracker_paths.items():
            setattr(tracker, key, value)

    def _restore_metrics_store_path(self):
        metrics_store.METRICS_DB_FILE = self.original_metrics_db_file

    def _sample_snapshot(self):
        return {
            "period": {"start": "02-21", "end": "03-22"},
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

    def test_save_and_get_latest_operations_snapshot(self):
        snapshot = self._sample_snapshot()

        tracker.save_operations_snapshot(snapshot)
        latest = tracker.get_latest_operations_snapshot()

        self.assertEqual(latest["metrics"]["views"], 32000)
        self.assertEqual(latest["traffic_sources"][0]["name"], "首页推荐")

    def test_snapshot_drives_execution_brief_without_historical_tracker_data(self):
        tracker.save_operations_snapshot(self._sample_snapshot())

        brief = strategy.get_data_driven_execution_brief()

        self.assertTrue(brief["has_data"])
        self.assertIn("首页推荐", brief["note"])
        self.assertGreaterEqual(len(brief["tool_focus"]), 1)
        self.assertGreaterEqual(len(brief["execution_focus"]), 1)

    def test_today_package_exposes_snapshot_execution_fields(self):
        tracker.save_operations_snapshot(self._sample_snapshot())

        with mock.patch("xhs_agent.calendar_engine.get_smart_recommendation", return_value={
            "date": "03月23日",
            "weekday": "周一",
            "recommended_time": "21:00",
            "priority": "weekday",
            "official_activities": [],
            "season": {"name": "春季", "colors": "粉绿"},
            "week_strategy": {"mood": "晚间更适合沉浸浏览", "avoid": "避免平铺直叙"},
            "upcoming_events": [],
            "reason": "测试用推荐",
        }):
            pkg = daily.get_today_package()

        self.assertIn("data_driven_note", pkg)
        self.assertIn("execution_focus", pkg)
        self.assertTrue(pkg["execution_focus"])

    def test_today_package_skips_already_published_content(self):
        tracker.add_post_record({
            "title": "名画破次元壁｜赵本山×范伟：中式喜剧遇上西方名画",
            "category": "画家故事",
            "content_type": "名画破次元壁",
            "post_date": "2026-03-17",
            "post_time": "21:00",
            "notes": "已发过",
        })

        real_datetime = datetime.datetime

        class FixedDateTime(real_datetime):
            @classmethod
            def now(cls, tz=None):
                return cls(2026, 3, 23, 12, 0, 0, tzinfo=tz)

        with mock.patch("xhs_agent.daily.datetime.datetime", FixedDateTime):
            with mock.patch("xhs_agent.calendar_engine.get_smart_recommendation", return_value={
                "date": "03月23日",
                "weekday": "周一",
                "recommended_time": "21:00",
                "priority": "weekday",
                "official_activities": [],
                "season": {"name": "春季", "colors": "粉绿"},
                "week_strategy": {"mood": "晚间更适合沉浸浏览", "avoid": "避免平铺直叙"},
                "upcoming_events": [],
                "reason": "测试用推荐",
            }):
                pkg = daily.get_today_package()

        self.assertNotEqual(pkg["title"], "名画破次元壁｜赵本山×范伟：中式喜剧遇上西方名画")

    def test_topic_id_blocks_similar_package_even_with_different_title(self):
        tracker.add_post_record({
            "title": "凌晨两点的便利店像一幅画",
            "topic_id": "creative-convenience-store-between-hopper-hockney",
            "category": "艺术灵感",
            "content_type": "风格对撞",
            "post_date": "2026-03-22",
            "post_time": "21:00",
            "notes": "已发过同主题",
        })

        real_datetime = datetime.datetime

        class FixedDateTime(real_datetime):
            @classmethod
            def now(cls, tz=None):
                return cls(2026, 3, 24, 12, 0, 0, tzinfo=tz)

        with mock.patch("xhs_agent.daily.datetime.datetime", FixedDateTime):
            with mock.patch("xhs_agent.calendar_engine.get_smart_recommendation", return_value={
                "date": "03月24日",
                "weekday": "周二",
                "recommended_time": "21:00",
                "priority": "weekday",
                "official_activities": [],
                "season": {"name": "春季", "colors": "粉绿"},
                "week_strategy": {"mood": "晚间更适合沉浸浏览", "avoid": "避免平铺直叙"},
                "upcoming_events": [],
                "reason": "测试用推荐",
            }):
                pkg = daily.get_today_package()

        self.assertNotEqual(pkg.get("topic_id"), "creative-convenience-store-between-hopper-hockney")

    def test_today_package_prefers_creative_pool_when_available(self):
        real_datetime = datetime.datetime

        class FixedDateTime(real_datetime):
            @classmethod
            def now(cls, tz=None):
                return cls(2026, 3, 24, 12, 0, 0, tzinfo=tz)

        with mock.patch("xhs_agent.daily.datetime.datetime", FixedDateTime):
            with mock.patch("xhs_agent.calendar_engine.get_smart_recommendation", return_value={
                "date": "03月24日",
                "weekday": "周二",
                "recommended_time": "21:00",
                "priority": "weekday",
                "official_activities": [],
                "season": {"name": "春季", "colors": "粉绿"},
                "week_strategy": {"mood": "晚间更适合沉浸浏览", "avoid": "避免平铺直叙"},
                "upcoming_events": [],
                "reason": "测试用推荐",
            }):
                pkg = daily.get_today_package()

        self.assertEqual(pkg.get("topic_id"), "creative-convenience-store-between-hopper-hockney")

    def test_today_package_uses_jay_klimt_topic_for_mar_30(self):
        real_datetime = datetime.datetime

        class FixedDateTime(real_datetime):
            @classmethod
            def now(cls, tz=None):
                return cls(2026, 3, 30, 12, 0, 0, tzinfo=tz)

        with mock.patch("xhs_agent.daily.datetime.datetime", FixedDateTime):
            with mock.patch("xhs_agent.calendar_engine.get_smart_recommendation", return_value={
                "date": "03月30日",
                "weekday": "周一",
                "recommended_time": "21:00",
                "priority": "weekday",
                "official_activities": [],
                "season": {"name": "春季", "colors": "粉绿"},
                "week_strategy": {"mood": "晚间更适合沉浸浏览", "avoid": "避免平铺直叙"},
                "upcoming_events": [],
                "reason": "测试用推荐",
            }):
                pkg = daily.get_today_package()

        self.assertEqual(pkg.get("topic_id"), "creative-jay-chou-klimt-easter-egg")
        self.assertEqual(pkg["title"], "周杰伦MV里最狠的，不是滤镜，是藏得最深的那幅名画")

    def test_adaptive_tool_profile_refreshes_when_snapshot_is_newer(self):
        tracker.save_account_info({"followers": 35})
        tracker._save_json(
            tracker.ANALYTICS_FILE,
            {
                "adaptive_tool_profile": {
                    "week_key": tracker._current_week_key(),
                    "generated_at": "2026-03-23T09:00:00",
                    "posting_focus": {"peak_hour_label": "23:00-24:00"},
                    "weekly_update_note": "旧档案",
                }
            },
        )

        tracker.save_operations_snapshot(
            {
                **self._sample_snapshot(),
                "viewer_time": {
                    "peak_window": "晚间",
                    "peak_hour_label": "近7日",
                },
                "recorded_at": "2026-03-30T09:00:00",
            }
        )

        profile = tracker.get_adaptive_tool_profile()

        self.assertEqual(profile["posting_focus"]["peak_hour_label"], "近7日")
        self.assertIn("近7日", profile["weekly_update_note"])

    def test_adaptive_tool_profile_refreshes_when_cached_snapshot_fields_drift(self):
        tracker.save_account_info({"followers": 35})
        tracker._save_json(
            tracker.ANALYTICS_FILE,
            {
                "adaptive_tool_profile": {
                    "week_key": tracker._current_week_key(),
                    "generated_at": "2026-03-30T09:37:54",
                    "posting_focus": {
                        "traffic_source": {"name": "首页推荐", "percent": 83},
                        "peak_hour_label": "23:00-24:00",
                    },
                    "weekly_update_note": "本周工具已按当前账号状态自动刷新：35粉，累计0篇笔记；近期主要流量来源是首页推荐 83%；高峰时段集中在23:00-24:00。",
                }
            },
        )

        tracker._save_json(
            tracker.OPERATIONS_SNAPSHOT_FILE,
            {
                "latest": {
                    **self._sample_snapshot(),
                    "viewer_time": {
                        "peak_window": "晚间",
                        "peak_hour_label": "近7日",
                    },
                    "recorded_at": "2026-03-30T09:00:00",
                },
                "snapshots": [],
            },
        )

        profile = tracker.get_adaptive_tool_profile()

        self.assertEqual(profile["posting_focus"]["peak_hour_label"], "近7日")
        self.assertIn("近7日", profile["weekly_update_note"])


if __name__ == "__main__":
    unittest.main()
