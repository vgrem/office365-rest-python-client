"""Server-side migration target — build a Migration API package and ingest it.

Unlike the client-side :class:`SharePointLibraryTarget` (which uploads each file
over REST), this target accumulates files/folders into a Migration API package,
stages the blobs in Azure Storage, and submits an ingestion job — the only path
that preserves version history and full ACL fidelity.

Content and manifest go to **different** containers; the caller supplies their SAS
URIs (e.g. from ``Site.provision_migration_containers``).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from office365.migration.base import MigrationItem
from office365.migration.package.builder import PackageBuilder
from office365.migration.package.staging import create_staging
from office365.migration.server_job import MigrationServerJob

if TYPE_CHECKING:
    from office365.migration.package.builder import Package

__all__ = ["SharePointPackageTarget"]


class SharePointPackageTarget:
    """A ``DataTarget`` that builds a package and submits a server-side ingestion job."""

    def __init__(
        self,
        site,
        web_id,
        *,
        content_uri: str | None = None,
        manifest_uri: str | None = None,
        site_url: str | None = None,
        list_title: str = "Documents",
        list_url: str | None = None,
        web_url: str = "/",
        azure_queue_report_uri: str | None = None,
        encryption_key: bytes | None = None,
        staging=None,
    ) -> None:
        self._site = site
        self._web_id = web_id
        self._list_title = list_title
        self._content_uri = content_uri
        self._manifest_uri = manifest_uri
        self._azure_queue_report_uri = azure_queue_report_uri
        self._encryption_key = encryption_key
        if staging is None:
            if not (content_uri and manifest_uri):
                raise ValueError("content_uri and manifest_uri are required unless staging is provided")
            staging = create_staging(content_uri, manifest_uri)
        self._staging = staging
        self._builder = PackageBuilder(
            site_url or getattr(site, "url", None) or "",
            web_id=web_id,
            web_url=web_url,
            list_title=list_title,
            list_url=list_url,
        )
        self.job_id: str | None = None
        self._package: "Package | None" = None

    def label(self) -> str:
        return f"migration-package:{self._list_title}"

    # ── DataTarget ───────────────────────────────────────────────

    def exists(self, item: MigrationItem) -> bool:
        # The server-side API handles overwrite/merge; nothing is checked client-side.
        return False

    def write(self, item: MigrationItem, payload: object) -> None:
        if item.item_type == "folder":
            self._builder.add_folder(
                item.dest_path,
                time_created=item.created,
                time_last_modified=item.modified,
            )
            return
        content = payload if isinstance(payload, bytes) else str(payload).encode("utf-8")
        self._builder.add_file(
            item.dest_path,
            content,
            time_created=item.created,
            time_last_modified=item.modified,
        )

    def list_paths(self) -> list[str]:
        return []

    def checksum(self, item: MigrationItem) -> str:
        return ""

    # ── Package + submission ─────────────────────────────────────

    def build(self) -> "Package":
        """Render the package from the items written so far."""
        self._package = self._builder.build()
        return self._package

    def stage(self) -> "Package":
        """Build the package and stage its blobs for ingestion."""
        package = self.build()
        self._staging.stage(package)
        return package

    def commit(self, options=None) -> None:
        """Stage the package and submit the ingestion job (called by the runner)."""
        if not (self._content_uri and self._manifest_uri):
            raise ValueError("content_uri and manifest_uri are required to submit an ingestion job")
        self.stage()
        server = MigrationServerJob(self._site)
        if self._encryption_key is not None:
            self.job_id = server.submit_encrypted(
                self._web_id,
                self._content_uri,
                self._manifest_uri,
                self._encryption_key,
                self._azure_queue_report_uri,
            )
        else:
            self.job_id = server.submit(
                self._web_id,
                self._content_uri,
                self._manifest_uri,
                self._azure_queue_report_uri,
            )

    def monitor(self, interval: float = 5, timeout: float = 1800, progress=None) -> str:
        """Poll the submitted job to completion (``GetMigrationJobProgress``)."""
        if self.job_id is None:
            raise ValueError("no job submitted yet — call commit() first")
        return MigrationServerJob(self._site).monitor(self.job_id, interval=interval, timeout=timeout, progress=progress)

    def close(self) -> None:
        pass
