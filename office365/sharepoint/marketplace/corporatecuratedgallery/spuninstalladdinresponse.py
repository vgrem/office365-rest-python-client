from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.spfailtotriggeruninstalladdinjobresponse import (
    SPFailToTriggerUninstallAddinJobResponse,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.sptriggereduninstalladdinjobresponse import (
    SPTriggeredUninstallAddinJobResponse,
)


@dataclass
class SPUninstallAddinResponse(ClientValue):
    executing: ClientValueCollection[SPTriggeredUninstallAddinJobResponse] = field(
        default_factory=lambda: ClientValueCollection(SPTriggeredUninstallAddinJobResponse)
    )
    failed: ClientValueCollection[SPFailToTriggerUninstallAddinJobResponse] = field(
        default_factory=lambda: ClientValueCollection(SPFailToTriggerUninstallAddinJobResponse)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPUninstallAddinResponse"
