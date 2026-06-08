from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.userprofiles.followed_item import FollowedItem


@dataclass
class FollowResult(ClientValue):
    """The FollowResult class returns information about a request to follow an item.

    Args:
        Item (FollowedItem): The Item property contains the item being followed.
        ResultType (int): The ResultType property provides information about the attempt to follow an item.
        For details on the FollowResultType type, see section 3.1.5.54.
    """

    Item: FollowedItem = field(default_factory=FollowedItem)
    ResultType: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.FollowResult"
