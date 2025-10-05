from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.timeframestatistics import TimeFrameStatistics


class ItemViewsAnalyticsData(ClientValue):

    def __init__(
        self,
        days: ClientValueCollection[TimeFrameStatistics] = ClientValueCollection(
            TimeFrameStatistics
        ),
        months: ClientValueCollection[TimeFrameStatistics] = ClientValueCollection(
            TimeFrameStatistics
        ),
    ):
        self.Days = days
        self.Months = months

    @property
    def entity_type_name(self):
        return "SP.Publishing.ItemViewsAnalyticsData"
