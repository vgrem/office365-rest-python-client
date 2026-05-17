from typing import Optional

from office365.runtime.client_value import ClientValue


class BookingQuestionAssignment(ClientValue):
    def __init__(self, is_required: Optional[bool] = None, question_id: Optional[str] = None):
        self.isRequired = is_required
        self.questionId = question_id

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingQuestionAssignment"
