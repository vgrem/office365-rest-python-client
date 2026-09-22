"""Tests for the server-side migration job (submit + progress parsing)."""

from __future__ import annotations

import json

from office365.migration.server_job import MigrationServerJob, parse_progress_events


class _Result:
    def __init__(self, value):
        self.value = value

    def execute_query(self):
        return self


class _Progress:
    def __init__(self, logs, next_token):
        self.Logs = logs
        self.NextToken = next_token


class _Site:
    url = "https://contoso.sharepoint.com/sites/x"

    def __init__(self, pages=None):
        self.calls: list = []
        self._pages = list(pages or [])

    def create_migration_ingestion_job(self, **kwargs):
        self.calls.append(("ingestion", kwargs))
        return _Result("job-1")

    def create_migration_job_encrypted(self, **kwargs):
        self.calls.append(("encrypted", kwargs))
        return _Result("job-2")

    def get_migration_job_progress(self, job_id, next_token):
        self.calls.append(("progress", job_id, next_token))
        page = self._pages.pop(0) if self._pages else ([], next_token)
        return _Result(_Progress(*page))


def test_parse_progress_events_reduces_to_status_and_counts():
    events = [
        {"Event": "JobQueued"},
        {"Event": "JobStart"},
        {"Event": "JobProgress", "ObjectsProcessed": "4", "TotalExpectedSPObjects": "10"},
        {"Event": "JobEnd", "ObjectsProcessed": "10", "TotalExpectedSPObjects": "10", "TotalErrors": "0"},
    ]
    assert parse_progress_events(events) == ("succeeded", 10, 10)


def test_parse_progress_events_marks_failed_on_errors():
    events = [{"Event": "JobEnd", "ObjectsProcessed": "3", "TotalErrors": "2"}]
    assert parse_progress_events(events)[0] == "failed"


def test_parse_progress_events_defaults_to_queued():
    assert parse_progress_events([]) == ("queued", 0, None)


def test_submit_and_submit_encrypted_use_the_right_methods():
    site = _Site()
    job = MigrationServerJob(site)

    assert job.submit("web", "src", "manifest") == "job-1"
    kind, kwargs = site.calls[0]
    assert kind == "ingestion"
    assert kwargs["g_web_id"] == "web"
    assert kwargs["ingestion_task_key"]

    assert job.submit_encrypted("web", "src", "manifest", b"key") == "job-2"
    kind, kwargs = site.calls[1]
    assert kind == "encrypted"
    assert kwargs["aes256_cbc_key"] == b"key"


def test_status_fn_accumulates_pages():
    pages = [
        (
            [
                json.dumps({"Event": "JobStart"}),
                json.dumps({"Event": "JobProgress", "ObjectsProcessed": "2", "TotalExpectedSPObjects": "5"}),
            ],
            "1",
        ),
        (
            [
                json.dumps(
                    {
                        "Event": "JobEnd",
                        "ObjectsProcessed": "5",
                        "TotalExpectedSPObjects": "5",
                        "TotalErrors": "0",
                    }
                )
            ],
            "2",
        ),
    ]
    status = MigrationServerJob(_Site(pages)).status_fn()

    assert status("job-1") == ("processing", 2, 5)
    assert status("job-1") == ("succeeded", 5, 5)


def test_monitor_returns_when_terminal():
    pages = [([json.dumps({"Event": "JobEnd", "TotalErrors": "0"})], "1")]
    assert MigrationServerJob(_Site(pages)).monitor("job-1", interval=0, timeout=5) == "succeeded"
