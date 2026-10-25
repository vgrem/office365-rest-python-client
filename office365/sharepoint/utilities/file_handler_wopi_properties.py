from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class FileHandlerWopiProperties(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "SP.Utilities.FileHandlerWopiProperties"

    @odata(name="FileGetUrl")
    @property
    def file_get_url(self) -> Optional[str]:
        """Gets the FileGetUrl property"""
        return self.properties.get("FileGetUrl", None)

    @odata(name="FileId")
    @property
    def file_id(self) -> Optional[str]:
        """Gets the FileId property"""
        return self.properties.get("FileId", None)

    @odata(name="FilePutUrl")
    @property
    def file_put_url(self) -> Optional[str]:
        """Gets the FilePutUrl property"""
        return self.properties.get("FilePutUrl", None)

    @odata(name="ResourceId")
    @property
    def resource_id(self) -> Optional[str]:
        """Gets the ResourceId property"""
        return self.properties.get("ResourceId", None)
