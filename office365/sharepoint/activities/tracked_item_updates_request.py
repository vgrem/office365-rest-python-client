from datetime import datetime

from office365.runtime.client_value import ClientValue


class TrackedItemUpdatesRequest(ClientValue):
    def __init__(
        self,
        timestamp=None,
        tracked_items_as_json=None,
        time_stamp: datetime = None,
        user_email: str = None,
        user_login: str = None,
        user_puid: str = None,
    ):
        """
        :param datetime timestamp:
        """
        self.TimeStamp = timestamp
        self.TrackedItemsAsJson = tracked_items_as_json
        self.TimeStamp = time_stamp
        self.UserEmail = user_email
        self.UserLogin = user_login
        self.UserPuid = user_puid

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.TrackedItemUpdatesRequest"
