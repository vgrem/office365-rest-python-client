from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class DynamicFaqSingalsData(ClientValue):
    def __init__(
        self,
        id_: Optional[str] = None,
        submitted_at: Optional[datetime] = None,
        submitted_question: Optional[str] = None,
    ):
        self.Id = id_
        self.SubmittedAt = submitted_at
        self.SubmittedQuestion = submitted_question

    @property
    def entity_type_name(self):
        return "SP.Publishing.DynamicFaqSingalsData"
