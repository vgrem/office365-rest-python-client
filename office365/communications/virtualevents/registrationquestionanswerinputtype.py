from enum import Enum


class VirtualEventRegistrationQuestionAnswerInputType(Enum):
    text = "0"
    multilineText = "1"
    singleChoice = "2"
    multiChoice = "3"
    boolean = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.VirtualEventRegistrationQuestionAnswerInputType"
