from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.security.threatintelligence.host import Host


class HostTracker(Entity):
    @odata(name="firstSeenDateTime")
    @property
    def first_seen_date_time(self) -> datetime:
        """Gets the firstSeenDateTime property"""
        return self.properties.get("firstSeenDateTime", datetime.min)

    @odata(name="kind")
    @property
    def kind(self) -> Optional[str]:
        """Gets the kind property"""
        return self.properties.get("kind", None)

    @odata(name="lastSeenDateTime")
    @property
    def last_seen_date_time(self) -> datetime:
        """Gets the lastSeenDateTime property"""
        return self.properties.get("lastSeenDateTime", datetime.min)

    @odata(name="value")
    @property
    def value(self) -> Optional[str]:
        """Gets the value property"""
        return self.properties.get("value", None)

    @odata(name="host", navigation=True)
    @property
    def host(self) -> Host:
        """Gets the host property"""
        return self.properties.get("host", Host(self.context, ResourcePath("host", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.HostTracker"
