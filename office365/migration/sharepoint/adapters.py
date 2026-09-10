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
from collections.abc import Callable
from typing import TYPE_CHECKING, cast

from office365.migration._util import emit_progress, record_to_json
from office365.migration.adapters import MigrationProgress
from office365.migration.base import MigrationItem
from office365.migration.sharepoint.transfer import Failure

if TYPE_CHECKING:
    from office365.sharepoint.files.file import File
    from office365.sharepoint.folders.folder import Folder
    from office365.sharepoint.lists.list import List as SPList

_TAXONOMY_FIELD_TYPES = {"TaxonomyFieldType", "TaxonomyFieldTypeMulti"}

# Read-only bookkeeping columns that add no content and can require extra
# permissions to project; never part of the fallback select.
_SYSTEM_INTERNAL_NAMES = {
    "ContentTypeId",
    "ContentType",
    "Created",
    "Modified",
    "Author",
    "Editor",
    "FileRef",
    "FileDirRef",
    "FileLeafRef",
    "File_x0020_Type",
    "FSObjType",
    "ID",
    "GUID",
    "UniqueId",
    "PermMask",
    "MetaInfo",
    "owshiddenversion",
    "AppAuthor",
    "AppEditor",
    "VirusStatus",
    "ScopeId",
    "InstanceID",
    "Order",
}


def is_taxonomy_validation(exc: Exception) -> bool:
    """True when a request failed because a Managed Metadata (taxonomy) column
    references a term set / term that no longer exists.

    SharePoint raises ``SPFieldValidationException`` ("the given guid does not
    exist in the term store") while composing the item payload — the exact case
    that makes a plain list-items read fail.
    """
    text = f"{getattr(exc, 'code', '') or ''} {getattr(exc, 'message', '') or ''} {exc}".lower()
    return "spfieldvalidationexception" in text and "term store" in text


def taxonomy_internal_names(fields) -> list[str]:
    """Internal names of Managed Metadata columns in a loaded field set."""
    names: list[str] = []
    for field in fields:
        type_name = getattr(field, "type_as_string", None) or ""
        schema = getattr(field, "schema_xml", None) or ""
        if type_name in _TAXONOMY_FIELD_TYPES or "TermSetId=" in schema:
            internal_name = getattr(field, "internal_name", None)
            if internal_name:
                names.append(internal_name)
    return list(dict.fromkeys(names))


class SharePointListSource:
    """Enumerates a SharePoint list's items into record migration items."""

    def __init__(self, source_list: "SPList", select: list[str] | None = None) -> None:
        self._list = source_list
        self._select = select
        self._records: dict[str, dict] = {}
        self.warnings: list[str] = []

    def label(self) -> str:
        return f"list:{self._list.title}"

    def list_items(self, progress: MigrationProgress = None) -> list[MigrationItem]:
        try:
            loaded = self._load_items(self._select)
        except Exception as e:  # noqa: BLE001 — see the taxonomy fallback below
            # A full read of a list with an orphaned Managed Metadata column
            # fails server-side; re-enumerate excluding those columns instead
            # of aborting the export. An explicit --select is honored as-is.
            if not is_taxonomy_validation(e) or self._select:
                raise
            self.warnings.append(
                "Full item read failed — a Managed Metadata column references a missing term set; "
                "re-read with taxonomy columns excluded."
            )
            try:
                loaded = self._load_items(self._safe_select())
            except Exception:
                # Some visible columns can still be denied to the principal;
                # fall back to the smallest possible projection.
                self.warnings.append("visible-column read denied too — exporting Id/Title only")
                loaded = self._load_items(["Id", "Title"])
        return self._project(loaded, progress)

    def _load_items(self, select: list[str] | None):
        items = self._list.items
        if select:
            items = items.select(select)
        return items.get_all().execute_query()

    def _safe_select(self) -> list[str]:
        """Fallback projection: visible, non-system columns minus Managed Metadata.

        Selecting hidden/system columns (``_Shortcut*``, ``MainLinkSettings``,
        taxonomy companion fields, ...) can itself be denied, so the fallback
        stays on the list's user columns only.
        """
        fields = self._list.fields.get().execute_query()
        taxonomy = taxonomy_internal_names(fields)
        self.warnings.append(f"excluded Managed Metadata column(s): {', '.join(sorted(taxonomy)) or 'none'}")
        columns = ["Id"]
        for field in fields:
            internal_name = getattr(field, "internal_name", None)
            if not internal_name or internal_name in taxonomy or internal_name in columns:
                continue
            if internal_name.startswith("_") or getattr(field, "hidden", False):
                continue  # hidden/system metadata — not safe to project
            if internal_name in _SYSTEM_INTERNAL_NAMES:
                continue
            columns.append(internal_name)
        return columns

    def _project(self, loaded, progress: MigrationProgress) -> list[MigrationItem]:
        result: list[MigrationItem] = []
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
            emit_progress(progress, done=len(result), stage="planning", items=[item])
        return result

    def read(self, item: MigrationItem) -> dict:
        return self._records.get(item.dest_path, {})

    def checksum(self, item: MigrationItem) -> str:
        payload = record_to_json(self._records.get(item.dest_path, {}))
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

    def list_paths(self) -> list[str]:
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
    """Enumerates a document library's files and folders (recursively) for migration.

    Folder entries (``item_type="folder"``, trailing ``/`` on the destination)
    preserve the folder structure — including **empty** folders — on the target.
    """

    def __init__(
        self,
        library_folder: "Folder",
        on_bytes: Callable[[int, int | None], None] | None = None,
    ) -> None:
        self._folder = library_folder
        self._files: dict[str, "File"] = {}
        # Optional hook invoked while a file downloads: (bytes_read, file_size)
        self.on_bytes = on_bytes

    def label(self) -> str:
        return f"library:{self._folder.server_relative_url}"

    def list_items(self, progress: MigrationProgress = None) -> list[MigrationItem]:
        # The root folder's URL may not be loaded yet (e.g. via
        # ``list.root_folder``); fetch it so destinations stay library-relative
        # instead of carrying the site/list path prefix.
        root = self._folder.server_relative_url
        if root is None:
            self._folder.ensure_properties(["ServerRelativeUrl"]).execute_query()
            root = self._folder.server_relative_url or ""
        root = root.rstrip("/")
        loaded_folders = self._folder.get_folders(recursive=True).execute_query()
        loaded = self._folder.get_files(recursive=True).execute_query()

        def _rel(url: str) -> str:
            return url[len(root) :].lstrip("/") if root else url.lstrip("/")

        result: list[MigrationItem] = []
        seen: set[str] = set()
        for folder in loaded_folders:
            url = folder.server_relative_url or ""
            rel = _rel(url)
            if not rel or rel in seen:
                continue
            seen.add(rel)
            result.append(MigrationItem(source_path=url, dest_path=f"{rel}/", item_type="folder"))
            emit_progress(progress, done=len(result), stage="planning", items=[folder])
        for file in loaded:
            url = file.server_relative_url or ""
            rel = _rel(url)
            self._files[rel] = file
            result.append(
                MigrationItem(
                    source_path=url,
                    dest_path=rel,
                    size_bytes=file.length or 0,
                    item_type="file",
                )
            )
            emit_progress(progress, done=len(result), stage="planning", items=[file])
        return result

    def read(self, item: MigrationItem) -> bytes:
        if item.item_type == "folder":
            return b""
        file = self._files.get(item.dest_path)
        if file is None:
            raise FileNotFoundError(item.source_path)
        buffer = io.BytesIO()
        total = file.length or 0

        def _chunk_downloaded(bytes_read: int) -> None:
            if self.on_bytes is not None:
                self.on_bytes(bytes_read, total or None)

        file.download_session(buffer, chunk_downloaded=_chunk_downloaded).execute_query()
        return buffer.getvalue()

    def checksum(self, item: MigrationItem) -> str:
        if item.item_type == "folder":
            return hashlib.md5(b"").hexdigest()
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
        items: list[MigrationItem],
        payloads: list[object],
        concurrency: int | None = None,
    ) -> list[Failure]:
        """Transfer a batch of items in parallel (fast path — the library-target transfer).

        Returns:
            List of ``(dest_path, error)`` for files that failed.
        """
        from office365.migration.sharepoint.transfer import _transfer_files_parallel

        files = [
            (item.dest_path, payload if isinstance(payload, bytes) else str(payload).encode("utf-8"))
            for item, payload in zip(items, payloads)
        ]
        return _transfer_files_parallel(
            self._folder,
            files,
            concurrency=concurrency or self._concurrency or 1,
        )

    def list_paths(self) -> list[str]:
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
