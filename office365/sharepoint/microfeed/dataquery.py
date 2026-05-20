from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class MicrofeedDataQuery(ClientValue):
    ItemLimit: Optional[int] = None
    Query: Optional[str] = None
    ViewFields: StringCollection = field(default_factory=StringCollection)
    ViewFieldsOnly: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedDataQuery"
