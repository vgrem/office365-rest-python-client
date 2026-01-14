from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.historyresult import (
    AmplifyPublishingHistoryResult,
)


class AmplifyPublishingHistory(ClientValue):
    def __init__(
        self,
        results: ClientValueCollection[AmplifyPublishingHistoryResult] = ClientValueCollection(
            AmplifyPublishingHistoryResult
        ),
    ):
        self.results = results

    @property
    def entity_type_name(self):
        return "SP.Publishing.AmplifyPublishingHistory"
