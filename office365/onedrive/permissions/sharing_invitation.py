from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


@dataclass
class SharingInvitation(ClientValue):
    """The SharingInvitation resource groups invitation-related data items into a single structure."""

    email: str | None = None
    invitedBy: IdentitySet | None = field(default_factory=IdentitySet)
    redeemedBy: str | None = None
    signInRequired: bool | None = None
