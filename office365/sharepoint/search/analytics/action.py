from datetime import datetime

from office365.runtime.client_value import ClientValue


class AnalyticsAction(ClientValue):
    def __init__(
        self,
        action_type: str = None,
        expire_time: datetime = None,
        properties: dict = None,
        user_time: datetime = None,
    ):
        """Represents the action in a Microsoft.SharePoint.Client.Search.Analytics.AnalyticsSignal Object."""
        self.ActionType = action_type
        self.ExpireTime = expire_time
        self.Properties = properties
        self.UserTime = user_time

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsAction"
