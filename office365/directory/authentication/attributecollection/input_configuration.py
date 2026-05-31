from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.attributecollection.inputtype import AuthenticationAttributeCollectionInputType
from office365.directory.authentication.attributecollection.option_configuration import (
    AuthenticationAttributeCollectionOptionConfiguration,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AuthenticationAttributeCollectionInputConfiguration(ClientValue):
    attribute: str | None = None
    defaultValue: str | None = None
    editable: bool | None = None
    hidden: bool | None = None
    inputType: AuthenticationAttributeCollectionInputType = AuthenticationAttributeCollectionInputType.text
    label: str | None = None
    options: ClientValueCollection[AuthenticationAttributeCollectionOptionConfiguration] = field(
        default_factory=lambda: ClientValueCollection(AuthenticationAttributeCollectionOptionConfiguration)
    )
    required: bool | None = None
    validationRegEx: str | None = None
    writeToDirectory: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationAttributeCollectionInputConfiguration"
