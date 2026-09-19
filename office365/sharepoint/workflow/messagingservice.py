from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class WorkflowMessagingService(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.WorkflowServices.WorkflowMessagingService"

    def publish_event(self, event_source_id: UUID, event_name: str, payload: dict) -> ClientResult[str]:
        """PublishEvent operation.

        Args:
            event_source_id (UUID): eventSourceId parameter
            event_name (str): eventName parameter
            payload (dict): payload parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "PublishEvent",
            None,
            {"eventSourceId": event_source_id, "eventName": event_name, "payload": payload},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
