from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


@dataclass
class PublicationFacet(ClientValue):
    """The publicationFacet resource provides details on the published status of a driveItemVersion or driveItem
    resource."""

    checkedOutBy: IdentitySet | None = field(default_factory=IdentitySet)
    level: str | None = None
    versionId: str | None = None
