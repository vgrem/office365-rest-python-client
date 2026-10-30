from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.security.threatintelligence.host import Host


class HostCookie(Entity):
    @odata(name="domain")
    @property
    def domain(self) -> Optional[str]:
        """Gets the domain property"""
        return self.properties.get("domain", None)

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

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="host", navigation=True)
    @property
    def host(self) -> Host:
        """Gets the host property"""
        return self.properties.get("host", Host(self.context, ResourcePath("host", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.HostCookie"
