from typing import Optional

from office365.sharepoint.listhome.item import ListHomeItem


class FavoriteListHomeItem(ListHomeItem):
    def __init__(
        self,
        favorites_order: Optional[float] = None,
        last_polled: Optional[float] = None,
        order: Optional[int] = None,
    ):
        super().__init__()
        self.favoritesOrder = favorites_order
        self.lastPolled = last_polled
        self.order = order

    " "

    @property
    def entity_type_name(self) -> str:  # type: ignore[override]
        return "Microsoft.SharePoint.ListHome.FavoriteListHomeItem"
