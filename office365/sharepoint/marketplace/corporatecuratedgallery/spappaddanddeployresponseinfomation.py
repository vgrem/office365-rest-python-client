from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPAppAddAndDeployResponseInfomation(ClientValue):
    IsFirstTimeDeployed: Optional[bool] = None
    ListId: Optional[str] = None
    ListItemId: Optional[str] = None
    ListItemUniqueId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAppAddAndDeployResponseInfomation"
