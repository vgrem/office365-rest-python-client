from __future__ import annotations

from office365.runtime.client_value import ClientValue


class PhysicalAddress(ClientValue):
    """The physical address of a contact."""

    city: str | None = None
    countryOrRegion: str | None = None
    postalCode: str | None = None
    state: str | None = None
    street: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.PhysicalAddress"
