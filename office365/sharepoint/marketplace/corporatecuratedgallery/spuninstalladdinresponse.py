from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.marketplace.corporatecuratedgallery.spfailtotriggeruninstalladdinjobresponse import (
    SPFailToTriggerUninstallAddinJobResponse,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.sptriggereduninstalladdinjobresponse import (
    SPTriggeredUninstallAddinJobResponse,
)


@value
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
