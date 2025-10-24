from enum import Enum


class MeetingAudience(Enum):
    everyone = "0"
    organization = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MeetingAudience"
