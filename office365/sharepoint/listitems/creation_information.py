from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ListItemCreationInformation(ClientValue):
    """
    Specifies the properties of the new list item.

    :param int underlying_object_type: Specifies whether the new list item is a file or a folder.
    :param str leaf_name: Specifies the name of the new list item. It MUST be the name of the file if the parent
        list of the list item is a document library.
    :param str folder_url: Specifies the folder for the new list item. It MUST be NULL, empty, a server-relative
        URL, or an absolute URL. If the value is a server-relative URL or an absolute URL, it MUST be under the root
        folder of the list.
    """

    FolderUrl: str | None = None
    LeafName: str | None = None
    UnderlyingObjectType: int | None = None
