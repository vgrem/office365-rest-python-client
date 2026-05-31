from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field

@dataclass
class AuthenticationAttributeCollectionPage(ClientValue):
    views: ClientValueCollection[AuthenticationAttributeCollectionPageViewConfiguration] = field(default_factory=lambda: ClientValueCollection(AuthenticationAttributeCollectionPageViewConfiguration))

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.AuthenticationAttributeCollectionPage'