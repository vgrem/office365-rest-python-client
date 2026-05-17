from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharepointids import SharePointIds


class InheritedFrom(ClientValue):
    def __init__(
        self,
        direct_url: Optional[str] = None,
        drive_id: Optional[str] = None,
        drive_type: Optional[str] = None,
        id_: Optional[str] = None,
        item_type: Optional[str] = None,
        name: Optional[str] = None,
        path: Optional[str] = None,
        share_id: Optional[str] = None,
        sharepoint_ids: SharePointIds = SharePointIds(),
    ):
        self.directUrl = direct_url
        self.driveId = drive_id
        self.driveType = drive_type
        self.id = id_
        self.itemType = item_type
        self.name = name
        self.path = path
        self.shareId = share_id
        self.sharepointIds = sharepoint_ids

    " "

    @property
    def entity_type_name(self):
        return "SP.Sharing.InheritedFrom"
