from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class AppIconInfo(Entity):
    @odata(name="Content")
    @property
    def content(self) -> Optional[bytes]:
        """Gets the Content property"""
        return self.properties.get("Content", None)

    @odata(name="MimeType")
    @property
    def mime_type(self) -> Optional[str]:
        """Gets the MimeType property"""
        return self.properties.get("MimeType", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Packaging.AppIconInfo"
