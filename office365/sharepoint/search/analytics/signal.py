from office365.runtime.client_value import ClientValue
from office365.sharepoint.search.analytics.action import AnalyticsAction
from office365.sharepoint.search.analytics.actor import AnalyticsActor
from office365.sharepoint.search.analytics.analyticsitem import AnalyticsItem


class AnalyticsSignal(ClientValue):
    def __init__(
        self,
        action: AnalyticsAction = AnalyticsAction(),
        actor: AnalyticsActor = AnalyticsActor(),
        item: AnalyticsItem = AnalyticsItem(),
        source: str = None,
    ):
        """Contains data about an action performed by an actor on an item."""
        self.Action = action
        self.Actor = actor
        self.Item = item
        self.Source = source

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsSignal"
