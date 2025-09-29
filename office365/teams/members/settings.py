from office365.runtime.client_value import ClientValue


class TeamMemberSettings(ClientValue):
    """Settings to configure whether members can perform certain actions, for example, create channels and add bots,
    in the team."""

    def __init__(
        self,
        allow_create_update_channels: bool = None,
        allow_delete_channels: bool = True,
        allow_add_remove_apps: bool = True,
        allow_create_update_remove_tabs: bool = True,
        allow_create_update_remove_connectors: bool = True,
    ):
        super().__init__()
        self.allowCreateUpdateChannels = allow_create_update_channels
        self.allowDeleteChannels = allow_delete_channels
        self.allowAddRemoveApps = allow_add_remove_apps
        self.allowCreateUpdateRemoveTabs = allow_create_update_remove_tabs
        self.allowCreateUpdateRemoveConnectors = allow_create_update_remove_connectors
