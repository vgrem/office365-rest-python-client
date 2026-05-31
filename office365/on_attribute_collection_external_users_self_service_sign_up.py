from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.paths.resource_path import ResourcePath
from office365.entity_collection import EntityCollection
from dataclasses import dataclass, field

@dataclass
class OnAttributeCollectionExternalUsersSelfServiceSignUp(ClientValue):
    attributeCollectionPage: AuthenticationAttributeCollectionPage = field(default_factory=AuthenticationAttributeCollectionPage)
    attributes: EntityCollection[IdentityUserFlowAttribute] | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.OnAttributeCollectionExternalUsersSelfServiceSignUp'