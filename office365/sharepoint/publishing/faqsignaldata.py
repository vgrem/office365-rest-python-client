from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.submitinfo import SubmitInfo


class FaqSignalData(ClientValue):
    def __init__(
        self,
        question_id: Optional[str] = None,
        signal_type: Optional[int] = None,
        submits: ClientValueCollection[SubmitInfo] = ClientValueCollection(SubmitInfo),
        value: Optional[int] = None,
    ):
        self.QuestionId = question_id
        self.SignalType = signal_type
        self.Submits = submits
        self.Value = value

    @property
    def entity_type_name(self):
        return "SP.Publishing.FaqSignalData"
