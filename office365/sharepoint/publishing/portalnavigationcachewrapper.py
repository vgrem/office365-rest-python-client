from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class PortalNavigationCacheWrapper(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.Navigation.PortalNavigationCacheWrapper"

    def disable(self) -> Self:
        """Disable operation."""
        qry = ServiceOperationQuery(self, "Disable", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def enable(self) -> Self:
        """Enable operation."""
        qry = ServiceOperationQuery(self, "Enable", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def refresh(self) -> Self:
        """Refresh operation."""
        qry = ServiceOperationQuery(self, "Refresh", None, {}, None, None)
        self.context.add_query(qry)
        return self
