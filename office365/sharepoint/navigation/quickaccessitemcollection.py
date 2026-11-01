from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class QuickAccessItemCollection(Entity):
    @staticmethod
    @site_access(SiteLevel.READ)
    def get_quick_access_items(context: ClientContext) -> ClientResult[str]:
        """GetQuickAccessItems operation."""
        from office365.sharepoint.navigation.quickaccessitemcollection import (
            QuickAccessItemCollection,
        )

        return_type = ClientResult(context, str())
        qry = FunctionQuery(QuickAccessItemCollection(context), "GetQuickAccessItems", [], return_type)
        context.add_query(qry)
        return return_type

    @staticmethod
    @site_access(SiteLevel.READ)
    def get_substrate_quick_access_items(context: ClientContext, top: int) -> ClientResult[str]:
        """GetSubstrateQuickAccessItems operation.

        Args:
            top (int):
                top parameter
        """
        from office365.sharepoint.navigation.quickaccessitemcollection import (
            QuickAccessItemCollection,
        )

        return_type = ClientResult(context, str())
        qry = FunctionQuery(QuickAccessItemCollection(context), "GetSubstrateQuickAccessItems", [top], return_type)
        context.add_query(qry)
        return return_type
