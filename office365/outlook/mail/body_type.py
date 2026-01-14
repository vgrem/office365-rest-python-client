from enum import Enum


class BodyType(Enum):
    html = "html"
    text = "text"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BodyType"
