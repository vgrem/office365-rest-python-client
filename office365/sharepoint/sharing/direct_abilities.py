from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus


@dataclass
class DirectSharingAbilities(ClientValue):
    """Represents the set of capabilities for direct sharing for the current user."""

    canAddExternalPrincipal: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canAddInternalPrincipal: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canRequestGrantAccess: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    supportsReviewPermission: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canAddNewExternalPrincipal: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canRequestGrantAccessForExistingExternalPrincipal: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canRequestGrantAccessForInternalPrincipal: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canRequestGrantAccessForNewExternalPrincipal: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    supportsEditPermission: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    supportsManageListPermission: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    supportsReadPermission: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    supportsRestrictedViewPermission: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)

    @property
    def entity_type_name(self):
        return "SP.Sharing.DirectSharingAbilities"
