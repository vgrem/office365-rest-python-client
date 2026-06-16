from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class PropertyValue(ClientValue):
    TermId: Optional[str] = None
    Value: Optional[str] = None
    id: UUID | None = None
    name: str | None = None
    sites: GuidCollection = field(default_factory=GuidCollection)

    @property
    def entity_type_name(self):
        return "SP.Publishing.PropertyValue"
