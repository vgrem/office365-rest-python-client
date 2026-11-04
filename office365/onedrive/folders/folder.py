from __future__ import annotations

from office365.onedrive.folders.view import FolderView
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class Folder(ClientValue):
    """
    The Folder resource groups folder-related data on an item into a single structure.
    DriveItems with a non-null folder facet are containers for other DriveItems.
    """

    childCount: int | None = None
    view: FolderView | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Folder"
