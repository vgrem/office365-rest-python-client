from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity


class PolicyDeletableItem(Entity):
    @property
    def deleted_date_time(self) -> Optional[datetime]:
        """Gets the deletedDateTime property"""
        return self.properties.get("deletedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PolicyDeletableItem"
