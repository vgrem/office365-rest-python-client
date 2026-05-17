from enum import Enum


class ExternalItemContentType(Enum):
    text = "1"
    html = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.externalConnectors.ExternalItemContentType"
