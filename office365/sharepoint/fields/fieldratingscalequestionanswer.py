from office365.runtime.client_value import ClientValue


class FieldRatingScaleQuestionAnswer(ClientValue):
    def __init__(self, answer: int = None, question: str = None):
        self.answer = answer
        self.question = question
