from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.workflow.instances.instance import WorkflowInstance


class WorkflowInstanceService(Entity):
    """Manages and reads workflow instances from the workflow host."""

    def enumerate_instances_for_site(self):
        """
        Returns the site workflow instances for the current site.
        """
        return_type = EntityCollection(self.context, WorkflowInstance)
        qry = ServiceOperationQuery(self, "EnumerateInstancesForSite", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.WorkflowServices.WorkflowInstanceService"

    @property
    def current(self) -> "WorkflowInstanceService":
        """Gets the Current property"""
        return self.properties.get(
            "Current", WorkflowInstanceService(self.context, ResourcePath("Current", self.resource_path))
        )

    def start_workflow_on_list_item_by_subscription_id(
        self, subscription_id: UUID, item_id: int, payload: dict
    ) -> ClientResult[str]:
        """StartWorkflowOnListItemBySubscriptionId operation.

        Args:
            subscription_id (UUID): subscriptionId parameter
            item_id (int): itemId parameter
            payload (dict): payload parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "StartWorkflowOnListItemBySubscriptionId",
            None,
            {"subscriptionId": subscription_id, "itemId": item_id, "payload": payload},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
