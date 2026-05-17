from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.spfailtotriggeruninstalladdinjobresponse import (
    SPFailToTriggerUninstallAddinJobResponse,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.sptriggereduninstalladdinjobresponse import (
    SPTriggeredUninstallAddinJobResponse,
)


class SPUninstallAddinResponse(ClientValue):
    def __init__(
        self,
        executing: ClientValueCollection[SPTriggeredUninstallAddinJobResponse] = ClientValueCollection(
            SPTriggeredUninstallAddinJobResponse
        ),
        failed: ClientValueCollection[SPFailToTriggerUninstallAddinJobResponse] = ClientValueCollection(
            SPFailToTriggerUninstallAddinJobResponse
        ),
    ):
        self.executing = executing
        self.failed = failed

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPUninstallAddinResponse"
