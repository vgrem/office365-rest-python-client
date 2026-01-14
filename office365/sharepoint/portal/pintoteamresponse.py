from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.portal.m365tabitem import M365TabItem


class PinToTeamResponse(ClientValue):
    def __init__(
        self,
        failed_pinning: ClientValueCollection[M365TabItem] = ClientValueCollection(M365TabItem),
        successful_pinning: ClientValueCollection[M365TabItem] = ClientValueCollection(M365TabItem),
    ):
        self.FailedPinning = failed_pinning
        self.SuccessfulPinning = successful_pinning

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.PinToTeamResponse"
