from __future__ import annotations

from dataclasses import dataclass

from office365.booking.phonetype import PhoneType
from office365.runtime.client_value import ClientValue


@dataclass
class Phone(ClientValue):
    language: str | None = None
    number: str | None = None
    region: str | None = None
    type: PhoneType | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.Phone"
