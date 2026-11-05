from __future__ import annotations

from dataclasses import field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


class PublicationFacet(ClientValue):
    """The publicationFacet resource provides details on the published status of a driveItemVersion or driveItem
    resource."""

    checkedOutBy: IdentitySet | None = field(default_factory=IdentitySet)
    level: str | None = None
    versionId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PublicationFacet"
