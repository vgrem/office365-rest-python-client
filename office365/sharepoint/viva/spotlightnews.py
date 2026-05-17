from office365.runtime.client_value import ClientValue
from typing import Optional


class SpotlightNews(ClientValue):
    def __init__(
        self,
        alt_text: Optional[str] = None,
        image_url: Optional[str] = None,
        is_boosted: Optional[bool] = None,
        order: Optional[int] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.AltText = alt_text
        self.ImageUrl = image_url
        self.IsBoosted = is_boosted
        self.Order = order
        self.Title = title
        self.Url = url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.SpotlightNews"
