from enum import Enum


class MobileAppPublishingState(Enum):
    notPublished = "0"
    processing = "1"
    published = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MobileAppPublishingState"
