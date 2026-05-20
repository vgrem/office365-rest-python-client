from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity import Identity
from office365.runtime.client_value import ClientValue


@dataclass
class IdentitySet(ClientValue):
    """
        The IdentitySet resource is a keyed collection of identity resources. It is used to represent a set of
    identities associated with various events for an item, such as created by or last modified by.
        Fields:
            application (Identity): The application associated with this action.
            device (Identity): The device associated with this action.
            user (Identity): The user associated with this action.
    """

    application: Identity = field(default_factory=Identity)
    device: Identity = field(default_factory=Identity)
    user: Identity = field(default_factory=Identity)

    def __repr__(self):
        return repr({n: v.to_json() for n, v in self if v.to_json()})
