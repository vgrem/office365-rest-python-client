from enum import Enum


class ConsentRequestFilterByCurrentUserOptions(Enum):
    reviewer = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConsentRequestFilterByCurrentUserOptions"
