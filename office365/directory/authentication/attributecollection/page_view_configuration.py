from __future__ import annotations

from dataclasses import field

from office365.directory.authentication.attributecollection.input_configuration import (
    AuthenticationAttributeCollectionInputConfiguration,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class AuthenticationAttributeCollectionPageViewConfiguration(ClientValue):
    description: str | None = None
    inputs: ClientValueCollection[AuthenticationAttributeCollectionInputConfiguration] = field(
        default_factory=lambda: ClientValueCollection(AuthenticationAttributeCollectionInputConfiguration)
    )
    title: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationAttributeCollectionPageViewConfiguration"
