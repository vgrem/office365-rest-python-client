from office365.runtime.client_value import ClientValue
from office365.sharepoint.sitedesigns.heroimage import HeroImage


class Section(ClientValue):

    def __init__(
        self,
        activity_image: str = None,
        activity_image_style: str = None,
        activity_text: str = None,
        activity_title: str = None,
        hero_image: HeroImage = HeroImage(),
        start_group: bool = None,
        text: str = None,
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
