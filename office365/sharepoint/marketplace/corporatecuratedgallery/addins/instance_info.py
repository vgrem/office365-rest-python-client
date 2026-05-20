from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPAddinInstanceInfo(ClientValue):
    """
    Fields:
    - appIdentifier: str
    - appInstanceId: str
    - tenantAppData: str
    - tenantAppDataUpdateTime: datetime
    - title: str
    """

    appIdentifier: Optional[str] = None
    appInstanceId: Optional[str] = None
    tenantAppData: Optional[str] = None
    tenantAppDataUpdateTime: Optional[datetime] = None
    title: Optional[str] = None
    appSource: Optional[str] = None
    appWebFullUrl: Optional[str] = None
    appWebId: Optional[str] = None
    appWebName: Optional[str] = None
    assetId: Optional[str] = None
    creationTimeUtc: Optional[datetime] = None
    currentSiteId: Optional[str] = None
    currentWebId: Optional[str] = None
    currentWebName: Optional[str] = None
    currentWebUrl: Optional[str] = None
    installedBy: Optional[str] = None
    installedSiteId: Optional[str] = None
    installedWebId: Optional[str] = None
    installedWebName: Optional[str] = None
    installedWebUrl: Optional[str] = None
    launchUrl: Optional[str] = None
    licensePurchaseTime: Optional[datetime] = None
    locale: Optional[str] = None
    productId: Optional[str] = None
    purchaserIdentity: Optional[str] = None
    status: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinInstanceInfo"
