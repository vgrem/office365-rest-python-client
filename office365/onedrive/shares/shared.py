from datetime import datetime

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


class Shared(ClientValue):
    def __init__(
        self,
        owner: IdentitySet = IdentitySet(),
        scope: str = None,
        shared_by=IdentitySet(),
        shared_datetime: datetime = None,
    ):
        """
        Represents a DriveItem that has been shared with others.
        Includes information about how the item is shared.

        Args:
            owner: The identity of the owner of the shared item.
            scope: Indicates the scope of how the item is shared:
                   "anonymous", "organization", or "users". Read-only.
            shared_by: The identity of the user who shared the item.
            shared_datetime: The UTC date and time when the item was shared. Read-only.
        """
        super().__init__()
        self.owner = owner
        self.scope = scope
        self.sharedBy = shared_by
        self.sharedDateTime = shared_datetime
