from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.principal import Principal


@dataclass
class LinkInvitation(ClientValue):
    """
    This class is used to identify the specific invitees for a tokenized sharing link,
    along with who invited them and when.

    Fields:
        invitedBy: Indicates the principal who invited the invitee to the tokenized sharing link.
        invitedOn: String representation of nullable DateTime value indicating when the invitee was invited
            to the tokenized sharing link.
        invitee: Indicates a principal who is invited to the tokenized sharing link.
    """

    invitedBy: Principal = field(default_factory=Principal)
    invitedOn: str | None = None
    invitee: Principal = field(default_factory=Principal)

    @property
    def entity_type_name(self):
        return "SP.Sharing.LinkInvitation"
