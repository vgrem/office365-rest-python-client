from __future__ import annotations

from dataclasses import field
from typing import Dict
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class AddIn(ClientValue):
    id: UUID | None = None
    properties: ClientValueCollection[Dict] = field(default_factory=lambda: ClientValueCollection(dict))
    type: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.AddIn"
