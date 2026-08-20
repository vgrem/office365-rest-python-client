from __future__ import annotations

from dataclasses import dataclass

from office365.directory.identities.providers.base import IdentityProviderBase
from office365.entity_collection import EntityCollection
from office365.runtime.client_value import ClientValue


@dataclass
class OnAuthenticationMethodLoadStartExternalUsersSelfServiceSignUp(ClientValue):
    identityProviders: EntityCollection[IdentityProviderBase] | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnAuthenticationMethodLoadStartExternalUsersSelfServiceSignUp"
