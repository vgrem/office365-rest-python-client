from office365.booking.customers.answerinputtype import AnswerInputType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class BookingQuestionAnswer(ClientValue):
    def __init__(
        self,
        answer: str = None,
        answer_input_type: AnswerInputType = AnswerInputType.none,
        answer_options: StringCollection = None,
        is_required: bool = None,
        question: str = None,
        question_id: str = None,
        selected_options: StringCollection = None,
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
