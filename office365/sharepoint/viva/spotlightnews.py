from office365.runtime.client_value import ClientValue


class SpotlightNews(ClientValue):

    def __init__(
        self,
        alt_text: str = None,
        image_url: str = None,
        is_boosted: bool = None,
        order: int = None,
        title: str = None,
        url: str = None,
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
