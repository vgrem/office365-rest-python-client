from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sitedesigns.heroimage import HeroImage


class Section(ClientValue):
    def __init__(
        self,
        activity_image: Optional[str] = None,
        activity_image_style: Optional[str] = None,
        activity_text: Optional[str] = None,
        activity_title: Optional[str] = None,
        hero_image: HeroImage = HeroImage(),
        start_group: Optional[bool] = None,
        text: Optional[str] = None,
    ):
        self.activityImage = activity_image
        self.activityImageStyle = activity_image_style
        self.activityText = activity_text
        self.activityTitle = activity_title
        self.heroImage = hero_image
        self.startGroup = start_group
        self.text = text

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.Section"
