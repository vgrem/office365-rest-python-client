from typing import Dict, Self

from office365.migration.assessment.base_scanner import BaseScanner
from office365.sharepoint.listitems.collection import ListItemCollection
from office365.sharepoint.lists.list import List


class ListScanner(BaseScanner[List]):

    def build_query(self):
        # type: () -> Self
        self._query_list_metadata()

        self._query_list_items()

        return self

    def process(self):
        # type: () -> Dict
        return {
            "ListTemplate": self.source.base_template,
            "NumOfAllItems": self.source.item_count,
            # "NumOfPages": -1,
            # "NumOfCheckedOutFiles": -1,
            # "NumOfItems_HasUniquePermission": -1,
            "NumOfUniquePermissions": (
                len(self.source.role_assignments)
                if self.source.has_unique_role_assignments
                else 0
            ),
            "NumOfContentTypes": len(self.source.content_types),
            "NumOfFields": len(self.source.fields),
            # "NumOfLookupFields": -1,
            # "TotalFileVersions": -1,
            # "Size": -1,
            "NumOfFiles": self._result["NumOfFiles"],
            "NumOfFolders": self._result["NumOfFolders"],
        }

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
        self.source.items.select(
            ["Id", "FSObjType", "FileLeafRef", "ContentTypeId"]
        ).get().paged(page_size=1000, page_loaded=self._process_item)

    def _process_item(self, items):
        # type: (ListItemCollection) -> None
        self._result.setdefault("NumOfFiles", 0)
        self._result.setdefault("NumOfFolders", 0)

        file_count = sum(1 for item in items if item.properties.get("FSObjType") == 0)
        folder_count = sum(1 for item in items if item.properties.get("FSObjType") == 1)
        self._result["NumOfFiles"] += file_count
        self._result["NumOfFolders"] += folder_count
