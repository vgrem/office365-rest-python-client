from __future__ import annotations

import json
from dataclasses import dataclass
from typing import IO, TYPE_CHECKING, Callable, Union

from office365.runtime.client_result import ClientResult
from office365.sharepoint.files.system_object_type import FileSystemObjectType
from office365.sharepoint.listitems.collection import ListItemCollection
from office365.sharepoint.listitems.listitem import ListItem

if TYPE_CHECKING:
    from office365.sharepoint.files.file import File
    from office365.sharepoint.folders.folder import Folder
    from office365.sharepoint.lists.list import List


@dataclass
class ExportListProgress:
    total_items: int = 0
    processed_items: int = 0
    current_item: Union[File, Folder, ListItem] = None


class ListExporter:
    """SharePoint list exporter with progress tracking"""

    @staticmethod
    def export(
        source_list: List,
        destination_file: IO,
        include_content: bool = False,
        item_exported: Callable[[ExportListProgress], None] = None,
    ) -> List:
        """Exports SharePoint List"""
        import zipfile

        progress = ExportListProgress()

        def _append_file(name: str, data):
            with zipfile.ZipFile(
                destination_file.name, "a", zipfile.ZIP_DEFLATED
            ) as zf:
                zf.writestr(name, data)

        def _download_content(list_item: ListItem) -> None:
            def _after_downloaded(result: ClientResult[bytes]) -> None:
                item_path = list_item.properties["FileRef"].replace(
                    source_list.root_folder.server_relative_url, ""
                )
                _append_file(item_path, result.value)

            list_item.file.get_content().after_execute(_after_downloaded)

        def _export_items(items: ListItemCollection) -> None:

            progress.processed_items += len(items)

            for item in items:
                item_path = str(item.id) + ".json"
                progress.current_item = item

                if item.file_system_object_type == FileSystemObjectType.File:
                    _append_file(item_path, json.dumps(item.to_json()))

                    if include_content:
                        _download_content(item)

                    if callable(item_exported):
                        item_exported(progress)

        def _get_items():
            progress.total_items = source_list.item_count
            (
                source_list.items.select(
                    [
                        "*",
                        "Id",
                        "FileRef",
                        "FileDirRef",
                        "FileLeafRef",
                        "FileSystemObjectType",
                    ]
                )
                .get()
                .paged(page_loaded=_export_items)
            )

        source_list.ensure_properties(
            ["SchemaXml", "RootFolder", "ItemCount"], _get_items
        )

        return source_list
