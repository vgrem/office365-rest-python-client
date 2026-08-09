from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identities.b2bidentityproviderstype import B2bIdentityProvidersType
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class InvitationRedemptionIdentityProviderConfiguration(ClientValue):
    fallbackIdentityProvider: B2bIdentityProvidersType = B2bIdentityProvidersType.azureActiveDirectory
    primaryIdentityProviderPrecedenceOrder: ClientValueCollection[B2bIdentityProvidersType] = field(
        default_factory=lambda: ClientValueCollection(B2bIdentityProvidersType)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InvitationRedemptionIdentityProviderConfiguration"
