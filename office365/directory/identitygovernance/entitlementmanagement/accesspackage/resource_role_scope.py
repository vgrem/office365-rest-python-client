from __future__ import annotations

from datetime import datetime

from office365.entity import Entity


class AccessPackageResourceRoleScope(Entity):
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageResourceRoleScope"
