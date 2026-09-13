from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class MoveSiteROState(Entity):
    def update_site_ro_state(self) -> Self:
        """UpdateSiteROState operation."""
        qry = ServiceOperationQuery(self, "UpdateSiteROState", None, {}, None, None)
        self.context.add_query(qry)
        return self
