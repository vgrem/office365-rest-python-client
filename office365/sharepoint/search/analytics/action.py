from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class AnalyticsAction(ClientValue):
    def __init__(
        self,
        action_type: Optional[str] = None,
        expire_time: Optional[datetime] = None,
        properties: Optional[dict] = None,
        user_time: Optional[datetime] = None,
    ):
        """Represents the action in a Microsoft.SharePoint.Client.Search.Analytics.AnalyticsSignal Object."""
        self.ActionType = action_type
        self.ExpireTime = expire_time
        self.Properties = properties
        self.UserTime = user_time

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsAction"
