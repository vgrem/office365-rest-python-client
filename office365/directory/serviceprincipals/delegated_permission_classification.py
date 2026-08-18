from __future__ import annotations

from typing import Optional

from office365.directory.policies.permissionclassificationtype import PermissionClassificationType
from office365.entity import Entity


class DelegatedPermissionClassification(Entity):
    @property
    def classification(self) -> PermissionClassificationType:
        """Gets the classification property"""
        return self.properties.get("classification", PermissionClassificationType.low)

    @property
    def permission_id(self) -> Optional[str]:
        """Gets the permissionId property"""
        return self.properties.get("permissionId", None)

    @property
    def permission_name(self) -> Optional[str]:
        """Gets the permissionName property"""
        return self.properties.get("permissionName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DelegatedPermissionClassification"
