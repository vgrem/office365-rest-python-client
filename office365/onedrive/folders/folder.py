from __future__ import annotations

from dataclasses import dataclass

from office365.onedrive.folders.view import FolderView
from office365.runtime.client_value import ClientValue


@dataclass
class Folder(ClientValue):
    """
    The Folder resource groups folder-related data on an item into a single structure.
    DriveItems with a non-null folder facet are containers for other DriveItems.
    """

    childCount: int | None = None
    view: FolderView | None = None
