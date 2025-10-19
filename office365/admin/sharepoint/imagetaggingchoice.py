from enum import Enum


class ImageTaggingChoice(Enum):
    disabled = "0"
    basic = "1"
    enhanced = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ImageTaggingChoice"
