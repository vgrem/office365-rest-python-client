from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class AuthenticationAttributeCollectionInputConfiguration(ClientValue):
    attribute: str | None = None
    defaultValue: str | None = None
    editable: bool | None = None
    hidden: bool | None = None
    inputType: AuthenticationAttributeCollectionInputType = AuthenticationAttributeCollectionInputType.text
    label: str | None = None
    options: ClientValueCollection[AuthenticationAttributeCollectionOptionConfiguration] = field(default_factory=lambda: ClientValueCollection(AuthenticationAttributeCollectionOptionConfiguration))
    required: bool | None = None
    validationRegEx: str | None = None
    writeToDirectory: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.AuthenticationAttributeCollectionInputConfiguration'