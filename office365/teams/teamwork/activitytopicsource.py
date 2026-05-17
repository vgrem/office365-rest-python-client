from enum import Enum


class TeamworkActivityTopicSource(Enum):
    entityUrl = "0"
    text = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamworkActivityTopicSource"
