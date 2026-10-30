from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class PrintServiceEndpoint(Entity):
    """Represents URI and identifying information for a print service instance."""

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="uri")
    @property
    def uri(self) -> Optional[str]:
        """Gets the uri property"""
        return self.properties.get("uri", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintServiceEndpoint"
