from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class GovernanceInsight(Entity):
    @odata(name="insightCreatedDateTime")
    @property
    def insight_created_date_time(self) -> Optional[datetime]:
        """Gets the insightCreatedDateTime property"""
        return self.properties.get("insightCreatedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GovernanceInsight"
