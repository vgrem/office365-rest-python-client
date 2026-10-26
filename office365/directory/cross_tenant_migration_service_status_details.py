from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.cross_tenant_migration_service_status import CrossTenantMigrationServiceStatus
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.error import Error


@dataclass
class CrossTenantMigrationServiceStatusDetails(ClientValue):
    errors: ClientValueCollection[Error] = field(default_factory=lambda: ClientValueCollection(Error))
    message: str | None = None
    service: str | None = None
    status: CrossTenantMigrationServiceStatus = CrossTenantMigrationServiceStatus.notStarted

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantMigrationServiceStatusDetails"
