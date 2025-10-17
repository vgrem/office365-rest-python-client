from typing import Optional

from office365.sharepoint.entity import Entity


class AppIconInfo(Entity):

    @property
    def content(self) -> Optional[bytes]:
        """Gets the Content property"""
        return self.properties.get("Content", None)

    @property
    def mime_type(self) -> Optional[str]:
        """Gets the MimeType property"""
        return self.properties.get("MimeType", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Packaging.AppIconInfo"
