from __future__ import annotations

from office365.sharepoint.listhome.item import ListHomeItem


class FavoriteListHomeItem(ListHomeItem):
    """ """

    favoritesOrder: float | None = None
    lastPolled: float | None = None
    order: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ListHome.FavoriteListHomeItem"
