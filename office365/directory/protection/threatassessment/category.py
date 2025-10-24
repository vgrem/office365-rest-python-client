from enum import Enum


class ThreatCategory(Enum):
    undefined = "0"
    spam = "1"
    phishing = "2"
    malware = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ThreatCategory"
