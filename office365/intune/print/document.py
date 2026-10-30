from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class PrintDocument(Entity):
    @odata(name="contentType")
    @property
    def content_type(self) -> Optional[str]:
        """Gets the contentType property"""
        return self.properties.get("contentType", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="downloadedDateTime")
    @property
    def downloaded_date_time(self) -> Optional[datetime]:
        """Gets the downloadedDateTime property"""
        return self.properties.get("downloadedDateTime", datetime.min)

    @odata(name="size")
    @property
    def size(self) -> Optional[int]:
        """Gets the size property"""
        return self.properties.get("size", None)

    @odata(name="uploadedDateTime")
    @property
    def uploaded_date_time(self) -> Optional[datetime]:
        """Gets the uploadedDateTime property"""
        return self.properties.get("uploadedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintDocument"
