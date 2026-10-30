from __future__ import annotations

from datetime import datetime

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class IntelligenceProfileIndicator(Entity):
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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.IntelligenceProfileIndicator"
