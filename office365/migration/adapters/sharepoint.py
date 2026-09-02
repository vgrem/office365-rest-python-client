"""SharePoint list source/target adapters (REST v1, via the records pipeline).

Migrates list items as records: the source projects loaded items with
``to_records``-style dictionaries and the target imports them with
``from_records`` (deferred, committed in batches). File/folder migrations use
the filesystem/upload adapters.

Lazy imports keep the migration core client-agnostic.
"""

from __future__ import annotations

import hashlib
import io
import json
from typing import TYPE_CHECKING, List, Optional, cast

from office365.migration.adapters import MigrationProgress
from office365.migration.adapters._transfer import Failure
from office365.migration.base import MigrationItem

if TYPE_CHECKING:
    from office365.sharepoint.files.file import File
    from office365.sharepoint.folders.folder import Folder
    from office365.sharepoint.lists.list import List as SPList


class SharePointListSource:
    """Enumerates a SharePoint list's items into record migration items."""

    def __init__(self, source_list: "SPList", select: Optional[List[str]] = None) -> None:
        self._list = source_list
        self._select = select
        self._records: dict[str, dict] = {}

    def label(self) -> str:
        return f"list:{self._list.title}"

    def list_items(self, progress: MigrationProgress = None) -> List[MigrationItem]:
        items = self._list.items
        if self._select:
            items = items.select(self._select)
        loaded = items.get_all().execute_query()

        result: List[MigrationItem] = []
        for item in loaded:
            record = {k: v for k, v in item.properties.items() if not str(k).startswith("__")}
            self._records[str(item.id)] = record
            result.append(
                MigrationItem(
                    source_path=f"{self._list.title}/{item.id}",
                    dest_path=str(item.id),
                    item_type="record",
                )
            )
            if callable(progress):
                from office365.runtime.operations import Progress

                progress(Progress(done=len(result), stage="planning", items=[item]))
        return result

    def read(self, item: MigrationItem) -> dict:
        return self._records.get(item.dest_path, {})

    def checksum(self, item: MigrationItem) -> str:
        payload = json.dumps(self._records.get(item.dest_path, {}), sort_keys=True)
        return hashlib.md5(payload.encode("utf-8")).hexdigest()

    def close(self) -> None:
        pass


class SharePointListTarget:
    """Imports record payloads into a SharePoint list via ``from_records``."""

    def __init__(self, target_list: "SPList") -> None:
        self._list = target_list

    def label(self) -> str:
        return f"list:{self._list.title}"

    def exists(self, item: MigrationItem) -> bool:
        return False  # records are appended; idempotency via manifest/checkpoint

    def write(self, item: MigrationItem, payload: object) -> None:
        self._list.items.from_records([cast(dict, payload)])

    def list_paths(self) -> List[str]:
        return [str(i.id) for i in self._list.items.get().execute_query()]

    def checksum(self, item: MigrationItem) -> str:
        return ""

    def commit(self, options=None) -> None:
        """Flush the queued record writes through an OData batch (JSON-only parallel mode)."""
        batch_size = getattr(options, "batch_size", None) or 100
        concurrency = getattr(options, "concurrency", None) or 1
        self._list.context.execute_batch(items_per_batch=batch_size, concurrency=concurrency)

    def close(self) -> None:
        pass


class SharePointLibrarySource:
    """Enumerates a document library's files (recursively) for migration."""

    def __init__(self, library_folder: "Folder") -> None:
        self._folder = library_folder
        self._files: dict[str, "File"] = {}

    def label(self) -> str:
        return f"library:{self._folder.server_relative_url}"

    def list_items(self, progress: MigrationProgress = None) -> List[MigrationItem]:
        root = (self._folder.server_relative_url or "").rstrip("/")
        loaded = self._folder.get_files(recursive=True).execute_query()

        result: List[MigrationItem] = []
        for file in loaded:
            url = file.server_relative_url or ""
            rel = url[len(root) :].lstrip("/") if root else url.lstrip("/")
            self._files[rel] = file
            result.append(
                MigrationItem(
                    source_path=url,
                    dest_path=rel,
                    size_bytes=file.length or 0,
                    item_type="file",
                )
            )
            if callable(progress):
                from office365.runtime.operations import Progress

                progress(Progress(done=len(result), stage="planning", items=[file]))
        return result

    def read(self, item: MigrationItem) -> bytes:
        file = self._files.get(item.dest_path)
        if file is None:
            raise FileNotFoundError(item.source_path)
        buffer = io.BytesIO()
        file.download(buffer).execute_query()
        return buffer.getvalue()

    def checksum(self, item: MigrationItem) -> str:
        return hashlib.md5(self.read(item)).hexdigest()

    def close(self) -> None:
        pass


class SharePointLibraryTarget:
    """Writes files into a document library, creating folders as needed.

    Uses the simple upload for files up to ~4MB; ``write_many`` (parallel,
    ``concurrency > 1``) uses ``create_upload_session`` for larger files.
    """

    def __init__(self, library_folder: "Folder", concurrency: int = 1) -> None:
        self._folder = library_folder
        self._concurrency = concurrency

    def label(self) -> str:
        return f"library:{self._folder.server_relative_url}"

    def _url(self, item: MigrationItem) -> str:
        return f"{(self._folder.server_relative_url or '').rstrip('/')}/{item.dest_path}"

    def exists(self, item: MigrationItem) -> bool:
        try:
            self._folder.context.web.get_file_by_server_relative_url(self._url(item)).get().execute_query()
            return True
        except Exception:  # noqa: BLE001 — a missing file surfaces as a request error
            return False

    def write(self, item: MigrationItem, payload: object) -> None:
        content = payload if isinstance(payload, bytes) else str(payload).encode("utf-8")
        self._folder.upload_file(item.dest_path, content).execute_query()

    def write_many(
        self,
        items: List[MigrationItem],
        payloads: List[object],
        concurrency: Optional[int] = None,
    ) -> List[Failure]:
        """Transfer a batch of items in parallel (fast path — the library-target transfer).

        Returns:
            List of ``(dest_path, error)`` for files that failed.
        """
        from office365.migration.adapters._transfer import _transfer_files_parallel

        files = [
            (item.dest_path, payload if isinstance(payload, bytes) else str(payload).encode("utf-8"))
            for item, payload in zip(items, payloads)
        ]
        return _transfer_files_parallel(
            self._folder,
            files,
            concurrency=concurrency or self._concurrency or 1,
        )

    def list_paths(self) -> List[str]:
        root = (self._folder.server_relative_url or "").rstrip("/")
        loaded = self._folder.get_files(recursive=True).execute_query()
        return [(f.server_relative_url or "")[len(root) :].lstrip("/") for f in loaded]

    def checksum(self, item: MigrationItem) -> str:
        file = self._folder.context.web.get_file_by_server_relative_url(self._url(item)).get().execute_query()
        buffer = io.BytesIO()
        file.download(buffer).execute_query()
        return hashlib.md5(buffer.getvalue()).hexdigest()

    def commit(self, options=None) -> None:
        pass

    def close(self) -> None:
        pass
