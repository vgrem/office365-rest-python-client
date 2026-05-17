from typing import Optional

from office365.runtime.client_value import ClientValue


class ChannelInfo(ClientValue):
    def __init__(
        self,
        description: Optional[str] = None,
        display_name: Optional[str] = None,
        files_folder_web_url: Optional[str] = None,
        id_: Optional[str] = None,
        member_ship_type: Optional[int] = None,
        web_url: Optional[str] = None,
    ):
        self.description = description
        self.displayName = display_name
        self.filesFolderWebUrl = files_folder_web_url
        self.id = id_
        self.memberShipType = member_ship_type
        self.webUrl = web_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.ChannelInfo"
