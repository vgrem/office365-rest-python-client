from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.unified_storage_quota import UnifiedStorageQuota


class StorageSettings(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.StorageSettings"

    @odata(name="quota", navigation=True)
    @property
    def quota(self) -> UnifiedStorageQuota:
        """Gets the quota property"""
        from office365.directory.unified_storage_quota import UnifiedStorageQuota

        return self.properties.get("quota", UnifiedStorageQuota(self.context, ResourcePath("quota", self.resource_path)))
