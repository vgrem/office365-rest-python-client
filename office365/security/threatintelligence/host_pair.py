from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.security.threatintelligence.host import Host


class HostPair(Entity):
    @odata(name="firstSeenDateTime")
    @property
    def first_seen_date_time(self) -> datetime:
        """Gets the firstSeenDateTime property"""
        return self.properties.get("firstSeenDateTime", datetime.min)

    @odata(name="lastSeenDateTime")
    @property
    def last_seen_date_time(self) -> datetime:
        """Gets the lastSeenDateTime property"""
        return self.properties.get("lastSeenDateTime", datetime.min)

    @odata(name="linkKind")
    @property
    def link_kind(self) -> Optional[str]:
        """Gets the linkKind property"""
        return self.properties.get("linkKind", None)

    @odata(name="childHost", navigation=True)
    @property
    def child_host(self) -> Host:
        """Gets the childHost property"""
        return self.properties.get("childHost", Host(self.context, ResourcePath("childHost", self.resource_path)))

    @odata(name="parentHost", navigation=True)
    @property
    def parent_host(self) -> Host:
        """Gets the parentHost property"""
        return self.properties.get("parentHost", Host(self.context, ResourcePath("parentHost", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.HostPair"
