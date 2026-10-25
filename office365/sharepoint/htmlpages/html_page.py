from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class HtmlPage(Entity):
    @odata(name="Id")
    @property
    def id_(self) -> Optional[int]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @property
    def entity_type_name(self) -> str:
        return "SP.HtmlPages.HtmlPage"

    @odata(name="Id")
    @property
    def id(self) -> Optional[int]:
        """Gets the Id property"""
        return self.properties.get("Id", None)
