from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.listhome.favorite_item import FavoriteListHomeItem


@value
class RecentAndJoinedTeamsResponse(ClientValue):
    joinedTeams: Optional[str] = None
    joinedTeamsError: Optional[int] = None
    joinedTeamsErrorCode: Optional[int] = None
    pinnedItems: ClientValueCollection[FavoriteListHomeItem] = field(
        default_factory=lambda: ClientValueCollection(FavoriteListHomeItem)
    )
    pinnedItemsError: Optional[str] = None
    pinnedItemsErrorCode: Optional[int] = None
    quickAccessItems: Optional[str] = None
    quickAccessItemsError: Optional[str] = None
    quickAccessItemsErrorCode: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.RecentAndJoinedTeamsResponse"
