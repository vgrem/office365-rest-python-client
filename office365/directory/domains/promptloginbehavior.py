from enum import Enum


class PromptLoginBehavior(Enum):
    translateToFreshPasswordAuthentication = "0"
    nativeSupport = "1"
    disabled = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PromptLoginBehavior"
