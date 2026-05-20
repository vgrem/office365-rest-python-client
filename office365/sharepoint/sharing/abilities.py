from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.direct_abilities import DirectSharingAbilities
from office365.sharepoint.sharing.link_abilities import SharingLinkAbilities
from office365.sharepoint.sharing.mainlinkabilities import MainLinkAbilities
from office365.sharepoint.sharing.settingsabilities import (
    SharingSettingsAbilities,
)


@dataclass
class SharingAbilities(ClientValue):
    """
    Represents the matrix of possible sharing abilities for direct sharing and tokenized sharing links along
    with the state of each capability for the current user.
    """

    anonymousLinkAbilities: SharingLinkAbilities = field(default_factory=SharingLinkAbilities)
    anyoneLinkAbilities: SharingLinkAbilities = field(default_factory=SharingLinkAbilities)
    directSharingAbilities: DirectSharingAbilities = field(default_factory=DirectSharingAbilities)
    organizationLinkAbilities: SharingLinkAbilities = field(default_factory=SharingLinkAbilities)
    peopleSharingLinkAbilities: SharingLinkAbilities = field(default_factory=SharingLinkAbilities)
    canStopSharing: bool | None = None
    mainLinkAbilities: MainLinkAbilities = field(default_factory=MainLinkAbilities)
    sharingSettingsAbilities: SharingSettingsAbilities = field(default_factory=SharingSettingsAbilities)

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingAbilities"
