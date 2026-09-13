from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.publishing.structuralnavigationcachestate import StructuralNavigationCacheState


class StructuralNavigationCacheWrapper(Entity):
    @property
    def entity_type_name(self):
        return "SP.Publishing.Navigation.StructuralNavigationCacheWrapper"

    def set_site_state(self, state: StructuralNavigationCacheState) -> Self:
        """SetSiteState operation.

        Args:
            state (StructuralNavigationCacheState): state parameter
        """
        qry = ServiceOperationQuery(self, "SetSiteState", None, {"state": state}, None, None)
        self.context.add_query(qry)
        return self

    def set_web_state(self, state: StructuralNavigationCacheState) -> Self:
        """SetWebState operation.

        Args:
            state (StructuralNavigationCacheState): state parameter
        """
        qry = ServiceOperationQuery(self, "SetWebState", None, {"state": state}, None, None)
        self.context.add_query(qry)
        return self

    def site_state(self) -> ClientResult[StructuralNavigationCacheState]:
        """SiteState operation."""
        return_type = ClientResult(self.context, StructuralNavigationCacheState())
        qry = FunctionQuery(self, "SiteState", [], return_type)
        self.context.add_query(qry)
        return return_type

    def web_state(self) -> ClientResult[StructuralNavigationCacheState]:
        """WebState operation."""
        return_type = ClientResult(self.context, StructuralNavigationCacheState())
        qry = FunctionQuery(self, "WebState", [], return_type)
        self.context.add_query(qry)
        return return_type
