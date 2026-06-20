from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity


class EdiscoveryCustodian(Entity):
    @property
    def acknowledged_date_time(self) -> Optional[datetime]:
        """Gets the acknowledgedDateTime property"""
        return self.properties.get("acknowledgedDateTime", datetime.min)

    @property
    def email(self) -> Optional[str]:
        """Gets the email property"""
        return self.properties.get("email", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryCustodian"
