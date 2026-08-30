"""SharePoint list source/target adapters (REST v1, via the records pipeline).

Migrates list items as records: the source projects loaded items with
``to_records``-style dictionaries and the target imports them with
``from_records`` (deferred, committed in batches). File/folder migrations use
the filesystem/upload adapters.

Lazy imports keep the migration core client-agnostic.
"""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING, List, Optional, cast

from office365.migration.adapters import MigrationProgress
from office365.migration.base import MigrationItem

if TYPE_CHECKING:
    from office365.sharepoint.lists.list import List as SPList


class SharePointListSource:
    """Enumerates a SharePoint list's items into record migration items."""

    def __init__(self, source_list: "SPList", select: Optional[List[str]] = None) -> None:
        self._list = source_list
        self._select = select
        self._records: dict[str, dict] = {}

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

    def exists(self, item: MigrationItem) -> bool:
        return False  # records are appended; idempotency via manifest/checkpoint

    def write(self, item: MigrationItem, payload: object) -> None:
        self._list.items.from_records([cast(dict, payload)])

    def list_paths(self) -> List[str]:
        return [str(i.id) for i in self._list.items.get().execute_query()]

    def checksum(self, item: MigrationItem) -> str:
        return ""

    def commit(self) -> None:
        self._list.context.execute_batch()

    def close(self) -> None:
        pass
