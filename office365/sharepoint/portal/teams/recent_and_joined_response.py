from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.listhome.favorite_item import FavoriteListHomeItem
from typing import Optional


class RecentAndJoinedTeamsResponse(ClientValue):
    def __init__(
        self,
        joined_teams: Optional[str] = None,
        joined_teams_error: Optional[int] = None,
        joined_teams_error_code: Optional[int] = None,
        pinned_items: ClientValueCollection[FavoriteListHomeItem] = ClientValueCollection(FavoriteListHomeItem),
        pinned_items_error: Optional[str] = None,
        pinned_items_error_code: Optional[int] = None,
        quick_access_items: Optional[str] = None,
        quick_access_items_error: Optional[str] = None,
        quick_access_items_error_code: Optional[int] = None,
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
