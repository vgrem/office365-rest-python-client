from office365.sharepoint.listhome.item import ListHomeItem


class FavoriteListHomeItem(ListHomeItem):

    def __init__(
        self,
        favorites_order: float = None,
        last_polled: float = None,
        order: int = None,
    ):
        super().__init__()
        self.favoritesOrder = favorites_order
        self.lastPolled = last_polled
        self.order = order

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ListHome.FavoriteListHomeItem"
