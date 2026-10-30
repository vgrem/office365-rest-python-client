from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class DomainDnsUnavailableRecord(Entity):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DomainDnsUnavailableRecord"
