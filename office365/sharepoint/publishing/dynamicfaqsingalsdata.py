from datetime import datetime

from office365.runtime.client_value import ClientValue


class DynamicFaqSingalsData(ClientValue):
    def __init__(
        self,
        id_: str = None,
        submitted_at: datetime = None,
        submitted_question: str = None,
    ):
        self.Id = id_
        self.SubmittedAt = submitted_at
        self.SubmittedQuestion = submitted_question

    @property
    def entity_type_name(self):
        return "SP.Publishing.DynamicFaqSingalsData"
