from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.sitedesigns.heroimage import HeroImage


@value
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
