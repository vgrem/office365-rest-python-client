from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.cross_tenant_migration_service_status_details import CrossTenantMigrationServiceStatusDetails
from office365.entity import Entity
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.cross_tenant_migration_cancel_response import CrossTenantMigrationCancelResponse


class CrossTenantMigrationTask(Entity):
    @odata(name="currentStatus")
    @property
    def current_status(self) -> ClientValueCollection[CrossTenantMigrationServiceStatusDetails]:
        """Gets the currentStatus property"""
        return self.properties.get(
            "currentStatus",
            ClientValueCollection[CrossTenantMigrationServiceStatusDetails](CrossTenantMigrationServiceStatusDetails),
        )

    @odata(name="lastUpdatedDateTime")
    @property
    def last_updated_date_time(self) -> Optional[datetime]:
        """Gets the lastUpdatedDateTime property"""
        return self.properties.get("lastUpdatedDateTime", datetime.min)

    @odata(name="taskType")
    @property
    def task_type(self) -> Optional[str]:
        """Gets the taskType property"""
        return self.properties.get("taskType", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantMigrationTask"

    def cancel(self) -> ClientResult[CrossTenantMigrationCancelResponse]:
        """cancel operation."""
        from office365.directory.cross_tenant_migration_cancel_response import CrossTenantMigrationCancelResponse

        return_type = ClientResult(self.context, CrossTenantMigrationCancelResponse())
        qry = ServiceOperationQuery(self, "cancel", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
