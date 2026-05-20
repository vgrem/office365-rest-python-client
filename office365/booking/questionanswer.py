from __future__ import annotations

from dataclasses import dataclass

from office365.booking.customers.answerinputtype import AnswerInputType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class BookingQuestionAnswer(ClientValue):
    answer: str | None = None
    answerInputType: AnswerInputType | None = None
    answerOptions: StringCollection | None = None
    isRequired: bool | None = None
    question: str | None = None
    questionId: str | None = None
    selectedOptions: StringCollection | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingQuestionAnswer"
