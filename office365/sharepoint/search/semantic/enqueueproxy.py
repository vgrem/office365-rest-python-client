from __future__ import annotations

from typing import TYPE_CHECKING

from office365.permissions.roles import DirectoryRole
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext
    from office365.sharepoint.search.semantic.crawlerenqueueitem import (
        SemanticSearchCrawlerEnqueueItem,
    )


class SemanticSearchEnqueueProxy(Entity):
    @staticmethod
    @site_access(SiteLevel.WRITE, role=DirectoryRole.SharePointAdministrator)
    def enqueue_item(context: ClientContext, item: SemanticSearchCrawlerEnqueueItem) -> None:
        """EnqueueItem operation.

        Args:
            item (SemanticSearchCrawlerEnqueueItem):
                item parameter
        """
        from office365.sharepoint.search.semantic.enqueueproxy import (
            SemanticSearchEnqueueProxy,
        )

        qry = ServiceOperationQuery(
            SemanticSearchEnqueueProxy(context), "EnqueueItem", None, {"item": item}, None, None, True
        )
        context.add_query(qry)

    @staticmethod
    @site_access(SiteLevel.WRITE, role=DirectoryRole.SharePointAdministrator)
    def enqueue_items(
        context: ClientContext, items: ClientValueCollection[SemanticSearchCrawlerEnqueueItem]
    ) -> ClientResult[ClientValueCollection[SemanticSearchCrawlerEnqueueItem]]:
        """EnqueueItems operation.

        Args:
            items (ClientValueCollection[SemanticSearchCrawlerEnqueueItem]):
                items parameter
        """
        from office365.sharepoint.search.semantic.crawlerenqueueitem import (
            SemanticSearchCrawlerEnqueueItem,
        )
        from office365.sharepoint.search.semantic.enqueueproxy import (
            SemanticSearchEnqueueProxy,
        )

        return_type = ClientResult(context, ClientValueCollection[SemanticSearchCrawlerEnqueueItem]())
        qry = ServiceOperationQuery(
            SemanticSearchEnqueueProxy(context), "EnqueueItems", None, {"items": items}, None, return_type, True
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    @site_access(SiteLevel.READ, role=DirectoryRole.SharePointAdministrator)
    def semantic_search_properties(context: ClientContext) -> ClientResult[bytes]:
        """SemanticSearchProperties operation."""
        from office365.sharepoint.search.semantic.enqueueproxy import (
            SemanticSearchEnqueueProxy,
        )

        return_type = ClientResult(context, bytes())
        qry = FunctionQuery(
            SemanticSearchEnqueueProxy(context), "SemanticSearchProperties", [], return_type, return_raw_content=True
        )
        context.add_query(qry)
        return return_type
