from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath


@dataclass
class ResourceFacet(ClientValue):
    """Fields:
    contentTypeId: The ID of the content type
    fileSystemObjectType: List item's object type in file system.
    fileType: The list item's file type
    itemId: Identifies the changed item.
    itemUniqueId: The Document identifier of the item
    """

    contentTypeId: Optional[str] = None
    fileSystemObjectType: Optional[int] = None
    fileType: Optional[int] = None
    itemId: Optional[str] = None
    itemUniqueId: Optional[str] = None
    listId: Optional[str] = None
    orgId: Optional[str] = None
    serverRelativePath: SPResPath = field(default_factory=SPResPath)
    siteId: Optional[str] = None
    title: Optional[str] = None
    webId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ResourceFacet"
