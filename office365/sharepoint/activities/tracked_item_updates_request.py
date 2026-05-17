from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class TrackedItemUpdatesRequest(ClientValue):
    def __init__(
        self,
        timestamp: datetime | None = None,
        tracked_items_as_json: str | None = None,
        user_email: str | None = None,
        user_login: str | None = None,
        user_puid: str | None = None,
    ):
        """
        :param datetime timestamp:
        """
        self.TimeStamp = timestamp
        self.TrackedItemsAsJson = tracked_items_as_json
        self.UserEmail = user_email
        self.UserLogin = user_login
        self.UserPuid = user_puid

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.TrackedItemUpdatesRequest"
