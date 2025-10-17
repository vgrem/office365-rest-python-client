from enum import Enum


class AnswerState(Enum):
    published = "0"
    draft = "1"
    excluded = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.search.AnswerState"
