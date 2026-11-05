from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue


class AnalyticsAction(ClientValue):
    """Represents the action in a Microsoft.SharePoint.Client.Search.Analytics.AnalyticsSignal Object."""

    ActionType: str | None = None
    ExpireTime: datetime | None = None
    Properties: dict = field(default_factory=dict)
    UserTime: datetime | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsAction"
