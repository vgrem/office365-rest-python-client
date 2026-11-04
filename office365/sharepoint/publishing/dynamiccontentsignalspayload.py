from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.publishing.dynamicfaqsingalsdata import DynamicFaqSingalsData
from office365.sharepoint.publishing.faqsignaldata import FaqSignalData


@value
class DynamicContentSignalsPayload(ClientValue):
    AdditionalData: ClientValueCollection[DynamicFaqSingalsData] = field(
        default_factory=lambda: ClientValueCollection(DynamicFaqSingalsData)
    )
    AggregatedData: ClientValueCollection[DynamicFaqSingalsData] = field(
        default_factory=lambda: ClientValueCollection(DynamicFaqSingalsData)
    )
    FaqSignals: ClientValueCollection[FaqSignalData] = field(
        default_factory=lambda: ClientValueCollection(FaqSignalData)
    )
    Id: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.DynamicContentSignalsPayload"
