from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.attributecollection.input_configuration import (
    AuthenticationAttributeCollectionInputConfiguration,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AuthenticationAttributeCollectionPageViewConfiguration(ClientValue):
    description: str | None = None
    inputs: ClientValueCollection[AuthenticationAttributeCollectionInputConfiguration] = field(
        default_factory=lambda: ClientValueCollection(AuthenticationAttributeCollectionInputConfiguration)
    )
    title: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationAttributeCollectionPageViewConfiguration"
