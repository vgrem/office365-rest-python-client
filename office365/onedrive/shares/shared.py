from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


@dataclass
class Shared(ClientValue):
    """
    Represents a DriveItem that has been shared with others.
    Includes information about how the item is shared.
    """

    owner: IdentitySet | None = field(default_factory=IdentitySet)
    scope: str | None = None
    sharedBy: IdentitySet | None = field(default_factory=IdentitySet)
    sharedDateTime: datetime | None = None
