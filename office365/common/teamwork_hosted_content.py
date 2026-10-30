from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class TeamworkHostedContent(Entity):
    @odata(name="contentBytes")
    @property
    def content_bytes(self) -> Optional[bytes]:
        """Gets the contentBytes property"""
        return self.properties.get("contentBytes", None)

    @odata(name="contentType")
    @property
    def content_type(self) -> Optional[str]:
        """Gets the contentType property"""
        return self.properties.get("contentType", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkHostedContent"
