"""Migration tasks — declarative source → target descriptors (SPMT ``Add-SPMTTask``).

Mirrors ``Microsoft.SharePoint.MigrationTool.PowerShell``'s task types:
**FileShare** (a local folder), **SharePoint** (a source site — all lists, or
selected ones), and **Json**-defined tasks (the ``-JsonDefinition`` format).
"""

from __future__ import annotations

import json
from dataclasses import dataclass

__all__ = ["FILE_SHARE", "SHAREPOINT", "MigrationTask"]

FILE_SHARE = "FileShare"
SHAREPOINT = "SharePoint"


@dataclass
class MigrationTask:
    """A declarative migration task (source → target mapping)."""

    kind: str = FILE_SHARE
    file_share_source: str | None = None
    sharepoint_source_site_url: str | None = None
    source_list: str | None = None
    source_list_relative_path: str | None = None
    target_site_url: str | None = None
    target_list: str | None = None
    target_list_relative_path: str | None = None
    migrate_all: bool = False
    migration_type: str = "Content"

    @classmethod
    def file_share(
        cls,
        source: str,
        target_site_url: str,
        target_list: str,
        target_list_relative_path: str | None = None,
    ) -> "MigrationTask":
        """A file-share task (``Add-SPMTTask -FileShareSource …``)."""
        return cls(
            kind=FILE_SHARE,
            file_share_source=source,
            target_site_url=target_site_url,
            target_list=target_list,
            target_list_relative_path=target_list_relative_path,
        )

    @classmethod
    def sharepoint(
        cls,
        source_site_url: str,
        target_site_url: str,
        *,
        source_list: str | None = None,
        target_list: str | None = None,
        source_list_relative_path: str | None = None,
        target_list_relative_path: str | None = None,
        migrate_all: bool = False,
    ) -> "MigrationTask":
        """A SharePoint task — ``migrate_all``, or a single ``source_list`` → ``target_list``."""
        return cls(
            kind=SHAREPOINT,
            sharepoint_source_site_url=source_site_url,
            source_list=source_list,
            source_list_relative_path=source_list_relative_path,
            target_site_url=target_site_url,
            target_list=target_list,
            target_list_relative_path=target_list_relative_path,
            migrate_all=migrate_all,
        )

    @classmethod
    def from_json(cls, definition: str | dict) -> "MigrationTask":
        """Parse an SPMT JSON task definition (``Add-SPMTTask -JsonDefinition``)."""
        data = json.loads(definition) if isinstance(definition, str) else dict(definition)
        if "Tasks" in data:  # a {"Tasks": [...]} wrapper → the first task
            tasks = data["Tasks"]
            if not tasks:
                raise ValueError("no tasks in the JSON definition")
            data = tasks[0]
        source = data.get("SourcePath")
        target = data.get("TargetPath")
        lists = (data.get("Items") or {}).get("Lists") or []
        if lists:
            first = lists[0]
            return cls(
                kind=SHAREPOINT,
                sharepoint_source_site_url=source,
                target_site_url=target,
                source_list=first.get("SourceList"),
                target_list=first.get("TargetList"),
            )
        return cls(
            kind=FILE_SHARE,
            file_share_source=source,
            target_site_url=target,
            target_list=data.get("TargetList"),
            target_list_relative_path=data.get("TargetListRelativePath"),
        )

    def to_json(self) -> str:
        """Serialize to the SPMT JSON task shape (round-trips through :meth:`from_json`)."""
        if self.kind == SHAREPOINT:
            data: dict = {"SourcePath": self.sharepoint_source_site_url, "TargetPath": self.target_site_url}
            if not self.migrate_all:
                data["Items"] = {"Lists": [{"SourceList": self.source_list, "TargetList": self.target_list}]}
        else:
            data = {
                "SourcePath": self.file_share_source,
                "TargetPath": self.target_site_url,
                "TargetList": self.target_list,
                "TargetListRelativePath": self.target_list_relative_path,
            }
        return json.dumps({name: value for name, value in data.items() if value is not None}, indent=2)

    def label(self) -> str:
        source = self.file_share_source or self.sharepoint_source_site_url or "?"
        return f"{self.kind}: {source} -> {self.target_site_url or '?'}"
