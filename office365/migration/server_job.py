"""SPMT-style server-side migration job — submit + monitor.

The SharePoint Migration API runs large migrations server-side: content is
packaged and uploaded to Azure Storage, then an *ingestion job* ingests it. This
wrapper submits such a job (``Site.create_migration_ingestion_job``) and polls
its status with a ``Progress`` hook, mirroring SPMT's task monitoring.

The status source is abstracted (``status_fn``) so callers can poll whichever
endpoint reports the job — e.g. the Azure report queue SPMT writes to, or the
Graph ``SharePointMigrationJob`` progress events.
"""

from __future__ import annotations

import time
import uuid
from typing import TYPE_CHECKING, Callable, Optional, Tuple

if TYPE_CHECKING:
    from office365.runtime.operations import Progress


class MigrationServerJob:
    """A server-side migration job: submit an ingestion job, then monitor it."""

    def __init__(self, site) -> None:
        self._site = site

    def submit(
        self,
        g_web_id,
        azure_container_source_uri: str,
        azure_container_manifest_uri: str,
        azure_queue_report_uri: str,
        ingestion_task_key: Optional[str] = None,
    ) -> str:
        """Submit an ingestion job and return its job id.

        Args:
            g_web_id: Identifier of the destination web.
            azure_container_source_uri: Azure container URI holding the data.
            azure_container_manifest_uri: Azure container URI holding the manifest.
            azure_queue_report_uri: Azure queue URI receiving progress reports.
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

    def monitor(
        self,
        job_id: str,
        status_fn: Callable[[str], Tuple[str, int, Optional[int]]],
        interval: int = 5,
        timeout: int = 1800,
        progress: Optional[Callable[["Progress"], None]] = None,
    ) -> str:
        """Poll a job until it reaches a terminal status.

        Args:
            job_id: The migration job id.
            status_fn: Callable returning ``(status, done, total)`` for a job id.
              ``done``/``total`` feed the ``Progress`` hook (total may be None).
            interval: Seconds between polls.
            timeout: Maximum seconds to wait before raising ``TimeoutError``.
            progress: Optional hook fired per poll with a ``Progress`` snapshot.

        Returns:
            The terminal status.

        Raises:
            TimeoutError: When the job doesn't finish within ``timeout`` seconds.
        """
        elapsed = 0
        while elapsed < timeout:
            status, done, total = status_fn(job_id)
            if callable(progress):
                from office365.runtime.operations import Progress

                progress(Progress(done=done, total=total, stage="migrating"))
            if status.lower() in ("succeeded", "completed", "failed", "cancelled"):
                return status
            time.sleep(interval)
            elapsed += interval
        raise TimeoutError(f"Migration job {job_id} did not finish within {timeout}s")
