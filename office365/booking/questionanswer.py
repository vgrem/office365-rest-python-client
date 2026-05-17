from typing import Optional

from office365.booking.customers.answerinputtype import AnswerInputType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class BookingQuestionAnswer(ClientValue):
    def __init__(
        self,
        answer: Optional[str] = None,
        answer_input_type: Optional[AnswerInputType] = None,
        answer_options: Optional[StringCollection] = None,
        is_required: Optional[bool] = None,
        question: Optional[str] = None,
        question_id: Optional[str] = None,
        selected_options: Optional[StringCollection] = None,
    ):
        self.answer = answer
        self.answerInputType = answer_input_type
        self.answerOptions = answer_options
        self.isRequired = is_required
        self.question = question
        self.questionId = question_id
        self.selectedOptions = selected_options

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingQuestionAnswer"
