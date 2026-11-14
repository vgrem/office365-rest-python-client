from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.service_storage_quota_breakdown import (
        ServiceStorageQuotaBreakdown,
    )


class UnifiedStorageQuota(Entity):
    @odata(name="deleted")
    @property
    def deleted(self) -> Optional[int]:
        """Gets the deleted property"""
        return self.properties.get("deleted", None)

    @odata(name="manageWebUrl")
    @property
    def manage_web_url(self) -> Optional[str]:
        """Gets the manageWebUrl property"""
        return self.properties.get("manageWebUrl", None)

    @odata(name="remaining")
    @property
    def remaining(self) -> Optional[int]:
        """Gets the remaining property"""
        return self.properties.get("remaining", None)

    @odata(name="state")
    @property
    def state(self) -> Optional[str]:
        """Gets the state property"""
        return self.properties.get("state", None)

    @odata(name="total")
    @property
    def total(self) -> Optional[int]:
        """Gets the total property"""
        return self.properties.get("total", None)

    @odata(name="used")
    @property
    def used(self) -> Optional[int]:
        """Gets the used property"""
        return self.properties.get("used", None)

    @odata(name="services", navigation=True)
    @property
    def services(self) -> EntityCollection[ServiceStorageQuotaBreakdown]:
        """Gets the services property"""
        from office365.directory.service_storage_quota_breakdown import (
            ServiceStorageQuotaBreakdown,
        )

        return self.properties.get(
            "services",
            EntityCollection[ServiceStorageQuotaBreakdown](
                self.context, ServiceStorageQuotaBreakdown, ResourcePath("services", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedStorageQuota"
