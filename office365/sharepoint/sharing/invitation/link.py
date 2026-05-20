from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.principal import Principal


@dataclass
class LinkInvitation(ClientValue):
    """This class is used to identify the specific invitees for a tokenized sharing link,
    along with who invited them and when."""

    invitedBy: Principal = field(default_factory=Principal)
    invitedOn: str | None = None
    invitee: Principal = field(default_factory=Principal)

    @property
    def entity_type_name(self):
        return "SP.Sharing.LinkInvitation"
