from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.itemsharingsettings import ItemSharingSettings
from office365.sharepoint.sharing.mainlinkinfo import MainLinkInfo


class MainAccessInformation(ClientValue):

    def __init__(
        self,
        default_main_link_role: int = None,
        main_link: MainLinkInfo = MainLinkInfo(),
        sharing_settings: ItemSharingSettings = ItemSharingSettings(),
    ):
        self.defaultMainLinkRole = default_main_link_role
        self.mainLink = main_link
        self.sharingSettings = sharing_settings

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainAccessInformation"
