from __future__ import annotations

from typing import Optional, Union


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath


@dataclass
class ListItemCreationInformationUsingPath(ClientValue):

    """
    Specifies the properties of the new list item.

    :param str leaf_name: Specifies the name of the list item that will be created. In the case of a document
    library, the name is equal to the filename of the list item.
    :param int object_type: Specifies the file system object type for the item that will be created.
    :param str or SPResPath folder_path: Specifies the path of the folder of the new list item.
    """

    LeafName: str
    UnderlyingObjectType: Optional[int] = None
    FolderPath: Optional[Union[str, SPResPath]] = None