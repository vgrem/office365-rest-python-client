from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class SPVivaLearningManager(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.Claims.SPVivaLearningManager"

    def register_list_event_receiver(self) -> Self:
        """RegisterListEventReceiver operation."""
        qry = ServiceOperationQuery(self, "RegisterListEventReceiver", None, {}, None, None)
        self.context.add_query(qry)
        return self
