from enum import Enum


class InferenceClassificationType(Enum):
    focused = "0"
    other = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.InferenceClassificationType"
