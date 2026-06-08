from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ListItemCreationInformation(ClientValue):
    """Specifies the properties of the new list item.

    Args:
        underlying_object_type (int): Specifies whether the new list item is a file or a folder.
        leaf_name (str): Specifies the name of the new list item. It MUST be the name of the file if the parent list of the list item is a document library.
        folder_url (str): Specifies the folder for the new list item. It MUST be NULL, empty, a server-relative URL, or an absolute URL. If the value is a server-relative URL or an absolute URL, it MUST be under the root folder of the list.
    """

    FolderUrl: str | None = None
    LeafName: str | None = None
    UnderlyingObjectType: int | None = None
