from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class CloudPcServicePlan(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="ramInGB")
    @property
    def ram_in_gb(self) -> Optional[int]:
        """Gets the ramInGB property"""
        return self.properties.get("ramInGB", None)

    @odata(name="storageInGB")
    @property
    def storage_in_gb(self) -> Optional[int]:
        """Gets the storageInGB property"""
        return self.properties.get("storageInGB", None)

    @odata(name="vCpuCount")
    @property
    def vcpu_count(self) -> Optional[int]:
        """Gets the vCpuCount property"""
        return self.properties.get("vCpuCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcServicePlan"
