from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharingInformationRequest(ClientValue):
    clientSupportedFeatures: str | None = None
    maxLinkMembersToReturn: int | None = None
    maxPrincipalsToReturn: int | None = None
    populateInheritedLinks: bool | None = None

    "Represents the optional Request Object for GetSharingInformation."

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingInformationRequest"
