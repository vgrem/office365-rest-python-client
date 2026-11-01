from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class APIHubConnector(Entity):
    @staticmethod
    @site_access(SiteLevel.WRITE)
    def invoke_query(context: ClientContext) -> ClientResult[bytes]:
        """InvokeQuery operation."""
        from office365.sharepoint.lists.apihubconnector import APIHubConnector

        return_type = ClientResult(context, bytes())
        qry = FunctionQuery(APIHubConnector(context), "InvokeQuery", [], return_type, return_raw_content=True)
        context.add_query(qry)
        return return_type
