from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class ExternalSubscriptionStore(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.BusinessData.Infrastructure.ExternalSubscriptionStore"

    def index_store(self) -> Self:
        """IndexStore operation."""
        qry = ServiceOperationQuery(self, "IndexStore", None, {}, None, None)
        self.context.add_query(qry)
        return self
