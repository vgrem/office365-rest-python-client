from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharepointids import SharePointIds


class InheritedFrom(ClientValue):
    def __init__(
        self,
        direct_url: str = None,
        drive_id: str = None,
        drive_type: str = None,
        id_: str = None,
        item_type: str = None,
        name: str = None,
        path: str = None,
        share_id: str = None,
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
