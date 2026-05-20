from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharingInformationRequest(ClientValue):
    """Represents the optional Request Object for GetSharingInformation."""

    clientSupportedFeatures: str | None = None
    maxLinkMembersToReturn: int | None = None
    maxPrincipalsToReturn: int | None = None
    populateInheritedLinks: bool | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingInformationRequest"
