from __future__ import annotations

from typing import Optional

from office365.directory.policies.permissionclassificationtype import PermissionClassificationType
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class DelegatedPermissionClassification(Entity):
    @odata(name="classification")
    @property
    def classification(self) -> PermissionClassificationType:
        """Gets the classification property"""
        return self.properties.get("classification", PermissionClassificationType.low)

    @odata(name="permissionId")
    @property
    def permission_id(self) -> Optional[str]:
        """Gets the permissionId property"""
        return self.properties.get("permissionId", None)

    @odata(name="permissionName")
    @property
    def permission_name(self) -> Optional[str]:
        """Gets the permissionName property"""
        return self.properties.get("permissionName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DelegatedPermissionClassification"
