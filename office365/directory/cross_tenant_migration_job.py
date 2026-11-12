from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.cross_tenant_migration_job_status import CrossTenantMigrationJobStatus
from office365.directory.cross_tenant_migration_job_type import CrossTenantMigrationJobType
from office365.directory.exchange_online_cross_tenant_migration_settings import (
    ExchangeOnlineCrossTenantMigrationSettings,
)
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.directory.cross_tenant_migration_cancel_response import CrossTenantMigrationCancelResponse
    from office365.directory.cross_tenant_migration_job import CrossTenantMigrationJob
    from office365.directory.cross_tenant_migration_task import CrossTenantMigrationTask


class CrossTenantMigrationJob(Entity):
    @odata(name="completeAfterDateTime")
    @property
    def complete_after_date_time(self) -> Optional[datetime]:
        """Gets the completeAfterDateTime property"""
        return self.properties.get("completeAfterDateTime", datetime.min)

    @odata(name="createdBy")
    @property
    def created_by(self) -> Optional[str]:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="exchangeSettings")
    @property
    def exchange_settings(self) -> Optional[ExchangeOnlineCrossTenantMigrationSettings]:
        """Gets the exchangeSettings property"""
        return self.properties.get("exchangeSettings", None)

    @odata(name="jobType")
    @property
    def job_type(self) -> Optional[CrossTenantMigrationJobType]:
        """Gets the jobType property"""
        return self.properties.get("jobType", None)

    @odata(name="lastUpdatedDateTime")
    @property
    def last_updated_date_time(self) -> Optional[datetime]:
        """Gets the lastUpdatedDateTime property"""
        return self.properties.get("lastUpdatedDateTime", datetime.min)

    @odata(name="message")
    @property
    def message(self) -> Optional[str]:
        """Gets the message property"""
        return self.properties.get("message", None)

    @odata(name="resources")
    @property
    def resources(self) -> StringCollection:
        """Gets the resources property"""
        return self.properties.get("resources", StringCollection())

    @odata(name="resourceType")
    @property
    def resource_type(self) -> Optional[str]:
        """Gets the resourceType property"""
        return self.properties.get("resourceType", None)

    @odata(name="sourceTenantId")
    @property
    def source_tenant_id(self) -> Optional[str]:
        """Gets the sourceTenantId property"""
        return self.properties.get("sourceTenantId", None)

    @odata(name="status")
    @property
    def status(self) -> Optional[CrossTenantMigrationJobStatus]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @odata(name="targetTenantId")
    @property
    def target_tenant_id(self) -> Optional[str]:
        """Gets the targetTenantId property"""
        return self.properties.get("targetTenantId", None)

    @odata(name="workloads")
    @property
    def workloads(self) -> StringCollection:
        """Gets the workloads property"""
        return self.properties.get("workloads", StringCollection())

    @odata(name="users", navigation=True)
    @property
    def users(self) -> EntityCollection[CrossTenantMigrationTask]:
        """Gets the users property"""
        from office365.directory.cross_tenant_migration_task import CrossTenantMigrationTask

        return self.properties.get(
            "users",
            EntityCollection[CrossTenantMigrationTask](
                self.context, CrossTenantMigrationTask, ResourcePath("users", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantMigrationJob"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["CrossTenantContentMigration.ReadWrite.All"],
        application=["CrossTenantContentMigration.ReadWrite.All"],
    )
    def cancel(self) -> ClientResult[CrossTenantMigrationCancelResponse]:
        """cancel operation."""
        from office365.directory.cross_tenant_migration_cancel_response import CrossTenantMigrationCancelResponse

        return_type = ClientResult(self.context, CrossTenantMigrationCancelResponse())
        qry = ServiceOperationQuery(self, "cancel", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["CrossTenantContentMigration.ReadWrite.All"],
        application=["CrossTenantContentMigration.ReadWrite.All"],
    )
    def migrate(self) -> CrossTenantMigrationJob:
        """migrate operation."""
        from office365.directory.cross_tenant_migration_job import CrossTenantMigrationJob

        return_type = CrossTenantMigrationJob(self.context)
        qry = ServiceOperationQuery(self, "migrate", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["CrossTenantContentMigration.ReadWrite.All"],
        application=["CrossTenantContentMigration.ReadWrite.All"],
    )
    def validate(self) -> CrossTenantMigrationJob:
        """validate operation."""
        from office365.directory.cross_tenant_migration_job import CrossTenantMigrationJob

        return_type = CrossTenantMigrationJob(self.context)
        qry = ServiceOperationQuery(self, "validate", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
