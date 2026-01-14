from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.dynamicfaqsingalsdata import DynamicFaqSingalsData
from office365.sharepoint.publishing.faqsignaldata import FaqSignalData


class DynamicContentSignalsPayload(ClientValue):
    def __init__(
        self,
        additional_data: ClientValueCollection[DynamicFaqSingalsData] = ClientValueCollection(DynamicFaqSingalsData),
        aggregated_data: ClientValueCollection[DynamicFaqSingalsData] = ClientValueCollection(DynamicFaqSingalsData),
        faq_signals: ClientValueCollection[FaqSignalData] = ClientValueCollection(FaqSignalData),
        id_: str = None,
    ):
        self.AdditionalData = additional_data
        self.AggregatedData = aggregated_data
        self.FaqSignals = faq_signals
        self.Id = id_

    @property
    def entity_type_name(self):
        return "SP.Publishing.DynamicContentSignalsPayload"
