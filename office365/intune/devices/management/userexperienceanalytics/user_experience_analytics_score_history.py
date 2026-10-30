from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsScoreHistory(Entity):
    @odata(name="startupDateTime")
    @property
    def startup_date_time(self) -> Optional[datetime]:
        """Gets the startupDateTime property"""
        return self.properties.get("startupDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsScoreHistory"
