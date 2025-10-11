from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.authpolicy.events.event import SPAuthEvent
from office365.sharepoint.authpolicy.events.role_assignment_resource_payload import (
    RoleAssignmentResourcePayload,
)
from office365.sharepoint.entity_collection import EntityCollection


class SPAuthEventCollection(EntityCollection[SPAuthEvent]):
    """Represents a collection of Field resource."""

    def __init__(self, context, resource_path=None, parent=None):
        super().__init__(context, SPAuthEvent, resource_path, parent)

    def role_assignment_ms_graph_notify(
        self,
        tenant: str,
        action: str,
        type_: str,
        resource_payload: RoleAssignmentResourcePayload,
        id_: str,
        container_id: str,
    ):
        """
        :param str tenant:
        :param str action:
        :param str type_:
        :param RoleAssignmentResourcePayload resource_payload:
        :param str id_:
        :param str container_id:
        """
        payload = {
            "tenant": tenant,
            "action": action,
            "type": type_,
            "resourcePayload": resource_payload,
            "id": id_,
            "containerId": container_id,
        }
        return_type = SPAuthEvent(self.context)
        self.add_child(return_type)
        qry = ServiceOperationQuery(self, "RoleAssignmentMSGraphNotify", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type
