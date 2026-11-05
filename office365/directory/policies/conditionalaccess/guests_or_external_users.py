from __future__ import annotations

from dataclasses import field

from office365.directory.policies.conditionalaccess.external_tenants import ConditionalAccessExternalTenants
from office365.directory.policies.conditionalaccess.guestorexternalusertypes import (
    ConditionalAccessGuestOrExternalUserTypes,
)
from office365.runtime.client_value import ClientValue


class ConditionalAccessGuestsOrExternalUsers(ClientValue):
    externalTenants: ConditionalAccessExternalTenants = field(default_factory=ConditionalAccessExternalTenants)
    guestOrExternalUserTypes: ConditionalAccessGuestOrExternalUserTypes = ConditionalAccessGuestOrExternalUserTypes.none

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessGuestsOrExternalUsers"
