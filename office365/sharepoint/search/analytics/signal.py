from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.search.analytics.action import AnalyticsAction
from office365.sharepoint.search.analytics.actor import AnalyticsActor
from office365.sharepoint.search.analytics.analyticsitem import AnalyticsItem


@dataclass
class AnalyticsSignal(ClientValue):
    """Contains data about an action performed by an actor on an item."""

    Action: AnalyticsAction = field(default_factory=AnalyticsAction)
    Actor: AnalyticsActor = field(default_factory=AnalyticsActor)
    Item: AnalyticsItem = field(default_factory=AnalyticsItem)
    Source: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsSignal"
