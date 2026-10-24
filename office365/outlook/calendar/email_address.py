from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.odata_property import Compare, odata


@dataclass
class EmailAddress(ClientValue):
    """The name and email address of a contact or message recipient.

    Fields:
        address (str | None): The email address of the person or entity.
        name (str | None): The display name of the person or entity.
    """

    #: Case-insensitive: the service does not distinguish ``Bob@x`` from ``bob@x``.
    address: str | None = field(default=None, metadata=odata("address", compare=Compare(casefold=True, key=True)))
    #: An address-only entry is read back named after its address (measured).
    name: str | None = field(default=None, metadata=odata("name", compare=Compare(fallback="address")))

    def __str__(self):
        return self.name or self.address or "(no email)"

    def __repr__(self):
        return f"{self.name or ''} <{self.address or ''}>"

    @property
    def entity_type_name(self):
        return None
