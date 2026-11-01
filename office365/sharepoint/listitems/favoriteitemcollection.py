from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class FavoriteItemCollection(Entity):
    @staticmethod
    @site_access(SiteLevel.READ)
    def get_favorite_items(context: ClientContext) -> ClientResult[str]:
        """GetFavoriteItems operation."""
        from office365.sharepoint.listitems.favoriteitemcollection import (
            FavoriteItemCollection,
        )

        return_type = ClientResult(context, str())
        qry = FunctionQuery(FavoriteItemCollection(context), "GetFavoriteItems", [], return_type)
        context.add_query(qry)
        return return_type
