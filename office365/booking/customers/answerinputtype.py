from enum import Enum


class AnswerInputType(Enum):
    text = "0"
    radioButton = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AnswerInputType"
