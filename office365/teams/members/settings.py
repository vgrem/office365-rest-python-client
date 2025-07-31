from office365.runtime.client_value import ClientValue


class TeamMemberSettings(ClientValue):
    """Settings to configure whether members can perform certain actions, for example, create channels and add bots,
    in the team."""

    def __init__(
        self,
        allow_create_update_channels: bool = None,
        allow_delete_channels: bool = True,
    ):
        super(TeamMemberSettings, self).__init__()
        self.allowCreateUpdateChannels = allow_create_update_channels
        self.allowDeleteChannels = allow_delete_channels
        self.allowAddRemoveApps = True
        self.allowCreateUpdateRemoveTabs = True
        self.allowCreateUpdateRemoveConnectors = True
