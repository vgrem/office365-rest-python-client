from enum import Enum


class SharingCapabilities(Enum):
    disabled = "0"
    externalUserSharingOnly = "1"
    externalUserAndGuestSharing = "2"
    existingExternalUserSharingOnly = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SharingCapabilities"
