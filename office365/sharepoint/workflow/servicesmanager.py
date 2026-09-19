from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.workflow.instances.service import WorkflowInstanceService


class WorkflowServicesManager(Entity):
    """Describes the workflow host configuration states and provides service objects that interact with the workflow."""

    def get_workflow_instance_service(self):
        """Returns the WorkflowInstanceService (manages and reads workflow instances from the workflow host),
        which manages workflow instances."""
        return_type = WorkflowInstanceService(self.context)
        qry = ServiceOperationQuery(self, "GetWorkflowInstanceService", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @staticmethod
    def current(context) -> "WorkflowServicesManager":
        """Specifies the current instance for the SP.TenantSettings.

        Args:
            context (office365.sharepoint.client_context.ClientContext):
        """
        return WorkflowServicesManager(context, ResourcePath("SP.WorkflowServices.WorkflowServicesManager.Current"))

    @property
    def entity_type_name(self):
        return "SP.WorkflowServices.WorkflowServicesManager"

    @property
    def app_id(self) -> Optional[str]:
        """Gets the AppId property"""
        return self.properties.get("AppId", None)

    @property
    def is_connected(self) -> Optional[bool]:
        """Gets the IsConnected property"""
        return self.properties.get("IsConnected", None)

    @property
    def is_registered(self) -> Optional[bool]:
        """Gets the IsRegistered property"""
        return self.properties.get("IsRegistered", None)

    @property
    def scope_path(self) -> Optional[str]:
        """Gets the ScopePath property"""
        return self.properties.get("ScopePath", None)

    @property
    def service_health_status(self) -> Optional[int]:
        """Gets the ServiceHealthStatus property"""
        return self.properties.get("ServiceHealthStatus", None)

    @property
    def workflow2013_retired(self) -> Optional[bool]:
        """Gets the Workflow2013Retired property"""
        return self.properties.get("Workflow2013Retired", None)

    def is_integrated_app(self) -> ClientResult[bool]:
        """IsIntegratedApp operation."""
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "IsIntegratedApp", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
