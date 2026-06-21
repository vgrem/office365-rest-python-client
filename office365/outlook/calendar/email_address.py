from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class EmailAddress(ClientValue):
    """The name and email address of a contact or message recipient.

    Fields:
        address (str | None): The email address of the person or entity.
        name (str | None): The display name of the person or entity.
    """

    address: str | None = None
    name: str | None = None

    def __str__(self):
        return self.name or self.address or "(no email)"

    def __repr__(self):
        return f"{self.name or ''} <{self.address or ''}>"

    @property
    def entity_type_name(self):
        return None
