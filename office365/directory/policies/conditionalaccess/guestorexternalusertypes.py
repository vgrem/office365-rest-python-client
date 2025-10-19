from enum import Enum


class ConditionalAccessGuestOrExternalUserTypes(Enum):
    none = "0"
    internalGuest = "1"
    b2bCollaborationGuest = "2"
    b2bCollaborationMember = "4"
    b2bDirectConnectUser = "8"
    otherExternalUser = "16"
    serviceProvider = "32"
    unknownFutureValue = "64"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConditionalAccessGuestOrExternalUserTypes"
