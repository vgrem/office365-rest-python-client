from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.publishing.timeframestatistics import TimeFrameStatistics


@value
class ItemViewsAnalyticsData(ClientValue):
    Days: ClientValueCollection[TimeFrameStatistics] = field(
        default_factory=lambda: ClientValueCollection(TimeFrameStatistics)
    )
    Months: ClientValueCollection[TimeFrameStatistics] = field(
        default_factory=lambda: ClientValueCollection(TimeFrameStatistics)
    )

    @property
    def entity_type_name(self):
        return "SP.Publishing.ItemViewsAnalyticsData"
