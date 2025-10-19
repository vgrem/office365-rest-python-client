from enum import Enum


class CloudAppSecuritySessionControlType(Enum):
    mcasConfigured = "0"
    monitorOnly = "1"
    blockDownloads = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudAppSecuritySessionControlType"
