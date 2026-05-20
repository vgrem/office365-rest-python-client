from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AddIn(ClientValue):
    id: UUID | None = None
    properties: ClientValueCollection[Dict] = field(default_factory=lambda: ClientValueCollection(dict))
    type: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.AddIn"
