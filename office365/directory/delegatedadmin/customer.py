from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.delegatedadmin.service_management_detail import (
        DelegatedAdminServiceManagementDetail,
    )


class DelegatedAdminCustomer(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @odata(name="serviceManagementDetails", navigation=True)
    @property
    def service_management_details(self) -> EntityCollection[DelegatedAdminServiceManagementDetail]:
        """Gets the serviceManagementDetails property"""
        from office365.directory.delegatedadmin.service_management_detail import (
            DelegatedAdminServiceManagementDetail,
        )

        return self.properties.get(
            "serviceManagementDetails",
            EntityCollection[DelegatedAdminServiceManagementDetail](
                self.context,
                DelegatedAdminServiceManagementDetail,
                ResourcePath("serviceManagementDetails", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DelegatedAdminCustomer"
