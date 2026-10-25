from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class RecentDocument(Entity):
    @odata(name="Application")
    @property
    def application(self) -> Optional[str]:
        """Gets the Application property"""
        return self.properties.get("Application", None)

    @odata(name="FileName")
    @property
    def file_name(self) -> Optional[str]:
        """Gets the FileName property"""
        return self.properties.get("FileName", None)

    @odata(name="IconUrl")
    @property
    def icon_url(self) -> Optional[str]:
        """Gets the IconUrl property"""
        return self.properties.get("IconUrl", None)

    @odata(name="IsPinned")
    @property
    def is_pinned(self) -> Optional[bool]:
        """Gets the IsPinned property"""
        return self.properties.get("IsPinned", None)

    @odata(name="LinkLocation")
    @property
    def link_location(self) -> Optional[str]:
        """Gets the LinkLocation property"""
        return self.properties.get("LinkLocation", None)

    @odata(name="TimeStamp")
    @property
    def time_stamp(self) -> datetime:
        """Gets the TimeStamp property"""
        return self.properties.get("TimeStamp", datetime.min)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.WebControls.RecentDocument"

    @odata(name="Id")
    @property
    def id(self) -> Optional[int]:
        """Gets the Id property"""
        return self.properties.get("Id", None)
