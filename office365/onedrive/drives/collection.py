from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.onedrive.drives.drive import Drive
from office365.runtime.paths.resource_path import ResourcePath

if TYPE_CHECKING:
    from office365.graph_client import GraphClient


class DriveCollection(EntityCollection[Drive]):
    def __init__(self, context: "GraphClient", resource_path: ResourcePath | None = None):
        super().__init__(context, Drive, resource_path)

    @require_permission(
        delegated=[
            "Files.Read",
            "Files.Read.All",
            "Files.ReadWrite",
            "Files.ReadWrite.All",
            "Sites.Read.All",
            "Sites.ReadWrite.All",
        ],
        application=["Files.Read.All", "Files.ReadWrite.All", "Sites.Read.All", "Sites.ReadWrite.All"],
        notes="List all drives in the tenant",
    )
    def get(self):
        """Retrieve drives"""
        return super().get()
