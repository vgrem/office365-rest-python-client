from enum import Enum


class FederatedIdpMfaBehavior(Enum):
    acceptIfMfaDoneByFederatedIdp = "0"
    enforceMfaByFederatedIdp = "1"
    rejectMfaByFederatedIdp = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.FederatedIdpMfaBehavior"
