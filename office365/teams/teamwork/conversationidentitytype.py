from enum import Enum


class TeamworkConversationIdentityType(Enum):
    team = "0"
    channel = "1"
    chat = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamworkConversationIdentityType"
