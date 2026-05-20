from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.spuninstalladdinerrordetail import (
    SPUninstallAddinErrorDetail,
)


@dataclass
class SPUninstallAddinJobDetail(ClientValue):
    absoluteUrl: Optional[str] = None
    appInstanceId: Optional[str] = None
    errorDetails: ClientValueCollection[SPUninstallAddinErrorDetail] = field(
        default_factory=lambda: ClientValueCollection(SPUninstallAddinErrorDetail)
    )
    jobId: Optional[str] = None
    serverRelativeUrl: Optional[str] = None
    siteId: Optional[str] = None
    taskStartTime: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPUninstallAddinJobDetail"
