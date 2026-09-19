from __future__ import annotations

from uuid import UUID

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class InteropService(Entity):
    @property
    def current(self) -> InteropService:
        """Gets the Current property"""
        return self.properties.get("Current", InteropService(self.context, ResourcePath("Current", self.resource_path)))

    @property
    def entity_type_name(self):
        return "SP.WorkflowServices.InteropService"

    def cancel_workflow(self, instance_id: UUID) -> Self:
        """CancelWorkflow operation.

        Args:
            instance_id (UUID): instanceId parameter
        """
        qry = ServiceOperationQuery(self, "CancelWorkflow", None, {"instanceId": instance_id}, None, None)
        self.context.add_query(qry)
        return self

    def disable_events(self, list_id: UUID, item_guid: UUID) -> Self:
        """DisableEvents operation.

        Args:
            list_id (UUID): listId parameter
            item_guid (UUID): itemGuid parameter
        """
        qry = ServiceOperationQuery(self, "DisableEvents", None, {"listId": list_id, "itemGuid": item_guid}, None, None)
        self.context.add_query(qry)
        return self

    def enable_events(self, list_id: UUID, item_guid: UUID) -> Self:
        """EnableEvents operation.

        Args:
            list_id (UUID): listId parameter
            item_guid (UUID): itemGuid parameter
        """
        qry = ServiceOperationQuery(self, "EnableEvents", None, {"listId": list_id, "itemGuid": item_guid}, None, None)
        self.context.add_query(qry)
        return self

    def start_workflow(
        self, association_name: str, correlation_id: UUID, list_id: UUID, item_guid: UUID, workflow_parameters: dict
    ) -> ClientResult[str]:
        """StartWorkflow operation.

        Args:
            association_name (str): associationName parameter
            correlation_id (UUID): correlationId parameter
            list_id (UUID): listId parameter
            item_guid (UUID): itemGuid parameter
            workflow_parameters (dict): workflowParameters parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "StartWorkflow",
            None,
            {
                "associationName": association_name,
                "correlationId": correlation_id,
                "listId": list_id,
                "itemGuid": item_guid,
                "workflowParameters": workflow_parameters,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
