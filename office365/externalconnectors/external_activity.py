from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.externalconnectors.activitytype import ExternalActivityType


class ExternalActivity(Entity):
    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @property
    def type_(self) -> ExternalActivityType:
        """Gets the type property"""
        return self.properties.get("type", ExternalActivityType.unknown)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ExternalActivity"
