from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.sharepointids import SharePointIds


@dataclass
class InheritedFrom(ClientValue):
    directUrl: str | None = None
    driveId: str | None = None
    driveType: str | None = None
    id: str | None = None
    itemType: str | None = None
    name: str | None = None
    path: str | None = None
    shareId: str | None = None
    sharepointIds: SharePointIds = field(default_factory=SharePointIds)

    " "

    @property
    def entity_type_name(self):
        return "SP.Sharing.InheritedFrom"
