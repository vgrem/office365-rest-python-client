from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.submitinfo import SubmitInfo


@dataclass
class FaqSignalData(ClientValue):
    QuestionId: Optional[str] = None
    SignalType: Optional[int] = None
    Submits: ClientValueCollection[SubmitInfo] = field(default_factory=lambda: ClientValueCollection(SubmitInfo))
    Value: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.FaqSignalData"
