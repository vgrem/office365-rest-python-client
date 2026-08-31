"""Offline tests for the SPMT-style server-side migration job wrapper."""

from __future__ import annotations

import unittest
from unittest import mock

from office365.migration import MigrationServerJob


class _Result:
    def __init__(self, value):
        self.value = value

    def execute_query(self):
        return self


class TestMigrationServerJob(unittest.TestCase):
    def test_submit_returns_job_id(self):
        site = mock.Mock()
        site.create_migration_ingestion_job.return_value = _Result("job-123")

        job = MigrationServerJob(site)
        job_id = job.submit("web-1", "uri/src", "uri/manifest", "uri/queue")

        self.assertEqual(job_id, "job-123")
        site.create_migration_ingestion_job.assert_called_once()
        kwargs = site.create_migration_ingestion_job.call_args.kwargs
        self.assertEqual(kwargs["g_web_id"], "web-1")
        self.assertTrue(kwargs["ingestion_task_key"])

    def test_monitor_reports_progress_and_terminal(self):
        statuses = iter([("running", 1, 10), ("running", 5, 10), ("succeeded", 10, 10)])
        seen = []
        job = MigrationServerJob(mock.Mock())

        def status_fn(job_id):
            return next(statuses)

        result = job.monitor(
            "job-1",
            status_fn,
            interval=0.01,
            timeout=10,
            progress=lambda p: seen.append((p.done, p.total)),
        )

        self.assertEqual(result, "succeeded")
        self.assertEqual([s[0] for s in seen], [1, 5, 10])  # noqa: PLR2004
        self.assertEqual(seen[-1][1], 10)  # noqa: PLR2004

    def test_monitor_times_out(self):
        job = MigrationServerJob(mock.Mock())

        with self.assertRaises(TimeoutError):
            job.monitor("job-1", lambda jid: ("running", 1, None), interval=0.01, timeout=0.05)


if __name__ == "__main__":
    unittest.main()
