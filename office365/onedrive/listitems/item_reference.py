from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.sharepoint_ids import SharePointIds
from office365.runtime.client_value import ClientValue


@dataclass
class ItemReference(ClientValue):
    """The ItemReference resource provides information necessary to address a DriveItem via the API."""

    id: str | None = None
    name: str | None = None
    path: str | None = None
    driveId: str | None = None
    driveType: str | None = None
    siteId: str | None = None
    sharepointIds: SharePointIds | None = field(default_factory=SharePointIds)
    shareId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ItemReference"
