from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus
from office365.sharepoint.sharing.linkexpirationabilitystatus import (
    SharingLinkExpirationAbilityStatus,
)
from office365.sharepoint.sharing.linkpasswordabilitystatus import (
    SharingLinkPasswordAbilityStatus,
)


@dataclass
class SharingLinkAbilities(ClientValue):
    """
    Represents the set of capabilities for specific configurations of tokenized sharing link for the current user
    and whether they are enabled or not.
    """

    canAddNewExternalPrincipals: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canDeleteEditLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canDeleteManageListLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canGetEditLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canGetReadLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canDeleteReadLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canDeleteRestrictedViewLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canDeleteReviewLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canDeleteSubmitOnlyLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canGetManageListLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canGetRestrictedViewLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canGetReviewLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canGetSubmitOnlyLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canHaveExternalUsers: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageEditLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageManageListLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageReadLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageRestrictedViewLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageReviewLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageSubmitOnlyLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    linkExpiration: SharingLinkExpirationAbilityStatus = field(default_factory=SharingLinkExpirationAbilityStatus)
    passwordProtected: SharingLinkPasswordAbilityStatus = field(default_factory=SharingLinkPasswordAbilityStatus)
    submitOnlylinkExpiration: SharingLinkExpirationAbilityStatus = field(
        default_factory=SharingLinkExpirationAbilityStatus
    )
    supportsRestrictedView: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    supportsRestrictToExistingRelationships: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    trackLinkUsers: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkAbilities"
