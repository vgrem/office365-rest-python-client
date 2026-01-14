from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.listhome.favorite_item import FavoriteListHomeItem


class RecentAndJoinedTeamsResponse(ClientValue):
    def __init__(
        self,
        joined_teams: str = None,
        joined_teams_error: int = None,
        joined_teams_error_code: int = None,
        pinned_items: ClientValueCollection[FavoriteListHomeItem] = ClientValueCollection(FavoriteListHomeItem),
        pinned_items_error: str = None,
        pinned_items_error_code: int = None,
        quick_access_items: str = None,
        quick_access_items_error: str = None,
        quick_access_items_error_code: int = None,
    ):
        self.joinedTeams = joined_teams
        self.joinedTeamsError = joined_teams_error
        self.joinedTeamsErrorCode = joined_teams_error_code
        self.pinnedItems = pinned_items
        self.pinnedItemsError = pinned_items_error
        self.pinnedItemsErrorCode = pinned_items_error_code
        self.quickAccessItems = quick_access_items
        self.quickAccessItemsError = quick_access_items_error
        self.quickAccessItemsErrorCode = quick_access_items_error_code

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.RecentAndJoinedTeamsResponse"
