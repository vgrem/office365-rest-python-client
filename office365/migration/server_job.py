"""Server-side migration job — submit + monitor.

The SharePoint Migration API runs large migrations server-side: content is
packaged and uploaded to Azure Storage, then an *ingestion job* ingests it. This
wrapper submits such a job and polls its status with a ``Progress`` hook.

Status can be read two ways:

- ``GetMigrationJobProgress`` — the recommended API; use :meth:`status_fn` as the
  ``monitor`` status source (or :meth:`progress` directly);
- a caller-supplied ``status_fn`` — e.g. an Azure queue or the Graph
  ``SharePointMigrationJobProgressEvent`` stream.
"""

from __future__ import annotations

import json
import time
import uuid
from collections.abc import Callable
from typing import TYPE_CHECKING

from office365.runtime.operations import emit_progress

if TYPE_CHECKING:
    from office365.runtime.operations import Progress

__all__ = ["MigrationServerJob", "job_errors", "parse_progress_events"]

_TERMINAL = ("succeeded", "completed", "failed", "cancelled")

# Migration API progress events -> monitor statuses (JobEnd resolved separately).
_EVENT_STATUS = {
    "JobQueued": "queued",
    "JobStart": "processing",
    "JobProgress": "processing",
    "JobError": "processing",
}


def parse_progress_events(events: list[dict]) -> tuple[str, int, int | None]:
    """Reduce accumulated Migration API progress events to ``(status, done, total)``.

    Pass the events accumulated across polls (they are append-only), so the status
    stays monotonic even when a poll returns no new events.
    """
    status = "queued"
    done = 0
    total: int | None = None
    for event in events:
        kind = event.get("Event")
        if kind == "JobEnd":
            status = "failed" if int(event.get("TotalErrors") or 0) else "succeeded"
        elif kind in _EVENT_STATUS:
            status = _EVENT_STATUS[kind]
        if event.get("ObjectsProcessed") is not None:
            done = int(event["ObjectsProcessed"])
        if event.get("TotalExpectedSPObjects") is not None:
            total = int(event["TotalExpectedSPObjects"])
    return status, done, total


def job_errors(events: list[dict]) -> list[dict]:
    """The ``JobError`` events from a progress log (each carries ``Message``/``ErrorType``/``Url``)."""
    return [event for event in events if event.get("Event") == "JobError"]


class MigrationServerJob:
    """A server-side migration job: submit an ingestion job, then monitor it."""

    def __init__(self, site) -> None:
        self._site = site

    def submit(
        self,
        g_web_id,
        azure_container_source_uri: str,
        azure_container_manifest_uri: str,
        azure_queue_report_uri: str | None = None,
        ingestion_task_key: str | None = None,
    ) -> str:
        """Submit an ingestion job for the staged package and return its job id.

        Args:
            g_web_id: Identifier of the destination web.
            azure_container_source_uri: Content container URI (with SAS token).
            azure_container_manifest_uri: Manifest container URI (with SAS token).
            azure_queue_report_uri: Optional Azure queue URI receiving progress reports.
            ingestion_task_key: Optional task key (a UUID is generated when omitted).
        """
        result = self._site.create_migration_ingestion_job(
            g_web_id=g_web_id,
            azure_container_source_uri=azure_container_source_uri,
            azure_container_manifest_uri=azure_container_manifest_uri,
            azure_queue_report_uri=azure_queue_report_uri,
            ingestion_task_key=ingestion_task_key or uuid.uuid4().hex,
        )
        return result.execute_query().value

    def submit_encrypted(
        self,
        g_web_id,
        azure_container_source_uri: str,
        azure_container_manifest_uri: str,
        aes256_cbc_key: str | bytes,
        azure_queue_report_uri: str | None = None,
    ) -> str:
        """Submit an ingestion job for an AES-256-CBC encrypted package.

        Required for SharePoint-provided containers; use the ``EncryptionKey`` from
        ``Site.provision_migration_containers`` (a base64 string, passed through).
        """
        result = self._site.create_migration_job_encrypted(
            g_web_id=g_web_id,
            azure_container_source_uri=azure_container_source_uri,
            azure_container_manifest_uri=azure_container_manifest_uri,
            aes256_cbc_key=aes256_cbc_key,
            azure_queue_report_uri=azure_queue_report_uri,
        )
        return result.execute_query().value

    def progress(self, job_id: str, next_token: str = "0") -> tuple[list[dict], str]:
        """Fetch a page of progress events and the next paging token.

        Args:
            job_id: The migration job id.
            next_token: Paging token; use ``"0"`` for the initial request.

        Returns:
            ``(events, next_token)`` — events are decoded from the JSON log strings.
        """
        result = self._site.get_migration_job_progress(job_id, next_token).execute_query()
        value = result.value
        events = [json.loads(line) for line in (value.Logs or [])]
        return events, value.NextToken or next_token

    def all_events(self, job_id: str) -> list[dict]:
        """All progress events for a job (paged until the token stops advancing).

        For a completed job the API is idempotent per token, so this collects the
        full lifecycle — including any ``JobError`` entries.
        """
        events: list[dict] = []
        token = "0"
        for _ in range(100):  # bound: a page with no new events ends the loop
            page, next_token = self.progress(job_id, token)
            events.extend(page)
            if not page or next_token == token:
                break
            token = next_token
        return events

    def errors(self, job_id: str) -> list[dict]:
        """The ``JobError`` events for a job (message, type, url)."""
        return job_errors(self.all_events(job_id))

    def status_fn(self) -> Callable[[str], tuple[str, int, int | None]]:
        """A ``monitor`` status function backed by ``GetMigrationJobProgress``."""
        state: dict = {"token": "0", "events": []}

        def _status(job_id: str) -> tuple[str, int, int | None]:
            events, token = self.progress(job_id, state["token"])
            state["token"] = token
            state["events"].extend(events)
            return parse_progress_events(state["events"])

        return _status

    def monitor(
        self,
        job_id: str,
        status_fn: Callable[[str], tuple[str, int, int | None]] | None = None,
        interval: float = 5,
        timeout: float = 1800,
        progress: Callable[["Progress"], None] | None = None,
    ) -> str:
        """Poll a job until it reaches a terminal status.

        Args:
            job_id: The migration job id.
            status_fn: Callable returning ``(status, done, total)`` for a job id.
              Defaults to a ``GetMigrationJobProgress``-backed reader.
            interval: Seconds between polls.
            timeout: Maximum seconds to wait before raising ``TimeoutError``.
            progress: Optional hook fired per poll with a ``Progress`` snapshot.

        Returns:
            The terminal status.

        Raises:
            TimeoutError: When the job doesn't finish within ``timeout`` seconds.
        """
        status_fn = status_fn or self.status_fn()
        elapsed = 0.0
        while elapsed < timeout:
            status, done, total = status_fn(job_id)
            emit_progress(progress, done=done, total=total, stage="migrating")
            if status.lower() in _TERMINAL:
                return status
            time.sleep(interval)
            elapsed += interval
        raise TimeoutError(f"Migration job {job_id} did not finish within {timeout}s")
