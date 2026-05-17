from enum import Enum


class AiInteractionType(Enum):
    userPrompt = "0"
    aiResponse = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AiInteractionType"
