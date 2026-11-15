from __future__ import annotations

from datetime import datetime

from office365.runtime.types.odata_property import odata
from office365.security.threatintelligence.indicator import Indicator


class IntelligenceProfileIndicator(Indicator):
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
