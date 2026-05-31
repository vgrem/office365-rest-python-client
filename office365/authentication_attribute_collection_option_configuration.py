from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from typing import Optional

@dataclass
class AuthenticationAttributeCollectionOptionConfiguration(ClientValue):
    label: str | None = None
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.AuthenticationAttributeCollectionOptionConfiguration'