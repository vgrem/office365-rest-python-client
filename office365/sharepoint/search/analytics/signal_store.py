from typing_extensions import Self

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.search.analytics.signal import AnalyticsSignal


class SignalStore(Entity):
    """Provides methods for managing the analytics signal store."""

    def __init__(self, context, resource_path):
        if resource_path is None:
            resource_path = ResourcePath("Microsoft.SharePoint.Client.Search.Analytics.SignalStore")
        super().__init__(context, resource_path)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.SignalStore"

    def signals(self, signals: ClientValueCollection[AnalyticsSignal]) -> Self:
        """signals operation.

        Args:
            signals (ClientValueCollection[AnalyticsSignal]): signals parameter
        """
        qry = ServiceOperationQuery(self, "signals", None, {"signals": signals}, None, None)
        self.context.add_query(qry)
        return self
