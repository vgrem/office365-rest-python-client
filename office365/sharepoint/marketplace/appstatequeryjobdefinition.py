from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class SPAppStateQueryJobDefinition(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.SPAppStateQueryJobDefinition"

    def perform_fast_revoke_with_client_ids(self) -> Self:
        """PerformFastRevokeWithClientIds operation."""
        qry = ServiceOperationQuery(self, "PerformFastRevokeWithClientIds", None, {}, None, None)
        self.context.add_query(qry)
        return self
