from office365.backuprestore.service_status import ServiceStatus
from office365.directory.permissions.require_permission import require_permission
from office365.directory.protection.policy.one_drive_for_business import (
    OneDriveForBusinessProtectionPolicy,
)
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata


class BackupRestoreRoot(Entity):
    """Represents the Microsoft 365 Backup Storage service in a tenant."""

    @require_permission(
        delegated=["BackupRestore-Control.ReadWrite.All"],
        application=["BackupRestore-Control.ReadWrite.All"],
    )
    def enable(self, app_owner_tenant_id: str) -> ClientResult[ServiceStatus]:
        """Enable the Microsoft 365 Backup Storage service for a tenant."""
        return_type = ClientResult(self.context, ServiceStatus())
        payload = {"appOwnerTenantId": app_owner_tenant_id}
        qry = ServiceOperationQuery(self, "enable", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="serviceStatus")
    @property
    def service_status(self) -> ServiceStatus:
        """Represents the tenant-level status of the Backup Storage service."""
        return self.properties.get("serviceStatus", ServiceStatus())

    @odata(name="oneDriveForBusinessProtectionPolicies")
    @property
    def one_drive_for_business_protection_policies(
        self,
    ) -> EntityCollection[OneDriveForBusinessProtectionPolicy]:
        """The list of OneDrive for Business restore sessions available in the tenant."""
        return self.properties.get(
            "oneDriveForBusinessProtectionPolicies",
            EntityCollection(
                self.context,
                OneDriveForBusinessProtectionPolicy,
                ResourcePath("oneDriveForBusinessProtectionPolicies", self.resource_path),
            ),
        )
