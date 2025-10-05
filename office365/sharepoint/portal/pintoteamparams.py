from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.portal.m365tabitem import M365TabItem


class PinToTeamParams(ClientValue):

    def __init__(
        self,
        tabs: ClientValueCollection[M365TabItem] = ClientValueCollection(M365TabItem),
        teams_id: str = None,
    ):
        self.tabs = tabs
        self.teamsId = teams_id
