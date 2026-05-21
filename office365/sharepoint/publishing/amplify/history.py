from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.historyresult import (
    AmplifyPublishingHistoryResult,
)


@dataclass
class AmplifyPublishingHistory(ClientValue):
    results: ClientValueCollection[AmplifyPublishingHistoryResult] = field(
        default_factory=lambda: ClientValueCollection(AmplifyPublishingHistoryResult)
    )

    @property
    def entity_type_name(self):
        return "SP.Publishing.AmplifyPublishingHistory"
