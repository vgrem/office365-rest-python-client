from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class AuthenticationAttributeCollectionPageViewConfiguration(ClientValue):
    description: str | None = None
    inputs: ClientValueCollection[AuthenticationAttributeCollectionInputConfiguration] = field(default_factory=lambda: ClientValueCollection(AuthenticationAttributeCollectionInputConfiguration))
    title: str | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.AuthenticationAttributeCollectionPageViewConfiguration'