from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharingLinkAccessRequest(ClientValue):
    """Represents extended values to include in a request for access to an object exposed through a tokenized
    sharing link."""

    ensureAccess: bool | None = None
    password: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkAccessRequest"
