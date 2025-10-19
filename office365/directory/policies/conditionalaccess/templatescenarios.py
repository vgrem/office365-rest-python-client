from enum import Enum


class TemplateScenarios(Enum):
    new = "0"
    secureFoundation = "1"
    zeroTrust = "2"
    remoteWork = "4"
    protectAdmins = "8"
    emergingThreats = "16"
    unknownFutureValue = "32"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TemplateScenarios"
