from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath


@dataclass
class ListItemCreationInformationUsingPath(ClientValue):
    """Specifies the properties of the new list item.

    Args:
        leaf_name (str): Specifies the name of the list item that will be created.
            In the case of a document library, the name is equal to the filename of the list item.
        object_type (int): Specifies the file system object type for the item that will be created.
        folder_path (str or SPResPath): Specifies the path of the folder of the new list item.
    """

    LeafName: str
    UnderlyingObjectType: Optional[int] = None
    FolderPath: Optional[Union[str, SPResPath]] = None
