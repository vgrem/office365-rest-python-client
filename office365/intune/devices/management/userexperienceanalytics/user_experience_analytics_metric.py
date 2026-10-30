from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsMetric(Entity):
    @odata(name="unit")
    @property
    def unit(self) -> Optional[str]:
        """Gets the unit property"""
        return self.properties.get("unit", None)

    @odata(name="value")
    @property
    def value(self) -> Optional[float]:
        """Gets the value property"""
        return self.properties.get("value", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsMetric"
