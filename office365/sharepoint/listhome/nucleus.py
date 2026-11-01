from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class Nucleus(Entity):
    @staticmethod
    @site_access(SiteLevel.MANAGE)
    def create_endpoint_list(context: ClientContext) -> None:
        """CreateEndpointList operation."""
        from office365.sharepoint.listhome.nucleus import Nucleus

        qry = ServiceOperationQuery(Nucleus(context), "CreateEndpointList", None, {}, None, None, True)
        context.add_query(qry)
