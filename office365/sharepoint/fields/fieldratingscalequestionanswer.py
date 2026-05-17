from typing import Optional

from office365.runtime.client_value import ClientValue


class FieldRatingScaleQuestionAnswer(ClientValue):
    def __init__(self, answer: Optional[int] = None, question: Optional[str] = None):
        self.answer = answer
        self.question = question
