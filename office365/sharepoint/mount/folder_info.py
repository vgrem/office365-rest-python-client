from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class MountedFolderInfo(Entity):
    """"""

    @odata(name="FolderUrl")
    @property
    def folder_url(self) -> Optional[str]:
        """Gets the FolderUrl property"""
        return self.properties.get("FolderUrl", None)

    @odata(name="HasEditPermission")
    @property
    def has_edit_permission(self) -> Optional[bool]:
        """Gets the HasEditPermission property"""
        return self.properties.get("HasEditPermission", None)

    @odata(name="ItemId")
    @property
    def item_id(self) -> Optional[int]:
        """Gets the ItemId property"""
        return self.properties.get("ItemId", None)

    @odata(name="ListTemplateType")
    @property
    def list_template_type(self) -> Optional[int]:
        """Gets the ListTemplateType property"""
        return self.properties.get("ListTemplateType", None)

    @odata(name="ListViewUrl")
    @property
    def list_view_url(self) -> Optional[str]:
        """Gets the ListViewUrl property"""
        return self.properties.get("ListViewUrl", None)

    @odata(name="WebUrl")
    @property
    def web_url(self) -> Optional[str]:
        """Gets the WebUrl property"""
        return self.properties.get("WebUrl", None)
