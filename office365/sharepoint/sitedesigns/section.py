from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sitedesigns.heroimage import HeroImage


@dataclass
class Section(ClientValue):
    activityImage: Optional[str] = None
    activityImageStyle: Optional[str] = None
    activityText: Optional[str] = None
    activityTitle: Optional[str] = None
    heroImage: HeroImage = field(default_factory=HeroImage)
    startGroup: Optional[bool] = None
    text: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.Section"
