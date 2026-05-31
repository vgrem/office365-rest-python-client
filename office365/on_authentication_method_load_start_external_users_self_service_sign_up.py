from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath

@dataclass
class OnAuthenticationMethodLoadStartExternalUsersSelfServiceSignUp(ClientValue):
    identityProviders: EntityCollection[IdentityProviderBase] | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.OnAuthenticationMethodLoadStartExternalUsersSelfServiceSignUp'