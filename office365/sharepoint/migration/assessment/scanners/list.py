from typing import Self

from office365.sharepoint.listitems.collection import ListItemCollection
from office365.sharepoint.lists.list import List
from office365.sharepoint.migration.assessment.scanners.base import BaseScanner, mapped_property


class ListScanner(BaseScanner[List]):

    @property
    def files_count(self):
        return self._properties.get("FilesCount", None)

    @property
    def folders_count(self):
        return self._properties.get("FoldersCount", None)

    @mapped_property("ItemsCount")
    def items_count(self):
        return self.source.item_count

    @mapped_property("FieldsCount")
    def fields_count(self):
        return len(self.source.fields)

    @mapped_property("ContentTypesCount")
    def content_types_count(self):
        return len(self.source.content_types)

    @property
    def list_template(self):
        return self.source.base_template

    def build_query(self) -> Self:
        self._query_list_metadata()

        self._query_list_items()

        return self

    def _query_list_metadata(self):
        self.source.select(
            [
                "Id",
                "Title",
                "IsCatalog",
                "BaseTemplate",
                "ItemCount",
                "SchemaXml",
                "LastItemModifiedDate",
                "RootFolder/ServerRelativeUrl",
                "ContentTypes/Name",
                "Fields/InternalName",
            ]
        ).expand(["RootFolder", "ContentTypes", "Fields"]).get()

    def _query_list_items(self):
        self.source.items.select(["Id", "FSObjType", "FileLeafRef", "ContentTypeId"]).get().paged(
            page_size=1000, page_loaded=self._process_item
        )

    def _process_item(self, items: ListItemCollection) -> None:
        self._properties.setdefault("FilesCount", 0)
        self._properties.setdefault("FoldersCount", 0)

        file_count = sum(1 for item in items if item.properties.get("FSObjType") == 0)
        folder_count = sum(1 for item in items if item.properties.get("FSObjType") == 1)
        self._properties["FilesCount"] += file_count
        self._properties["FoldersCount"] += folder_count
