from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPMachineLearningPublicationEntityData(ClientValue):
    ModelUniqueId: Optional[str] = None
    RemoveSitePromotionEnabled: Optional[bool] = None
    TargetLibraryServerRelativeUrl: Optional[str] = None
    TargetSiteUrl: Optional[str] = None
    TargetTableListServerRelativeUrl: Optional[str] = None
    TargetWebServerRelativeUrl: Optional[str] = None
    ViewOption: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningPublicationEntityData"
