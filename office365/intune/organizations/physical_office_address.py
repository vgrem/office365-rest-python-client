from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PhysicalOfficeAddress(ClientValue):
    city: str | None = None
    countryOrRegion: str | None = None
    officeLocation: str | None = None
    postalCode: str | None = None
    state: str | None = None
    street: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PhysicalOfficeAddress"
