from office365.runtime.client_value import ClientValue
from office365.sharepoint.news.itemreference import ItemReference


class NewsSite(ClientValue):

    def __init__(
        self,
        acronym: str = None,
        banner_color: str = None,
        banner_image_url: str = None,
        item_reference: ItemReference = ItemReference(),
        title: str = None,
        type_: str = None,
        url: str = None,
    ):
        self.Acronym = acronym
        self.BannerColor = banner_color
        self.BannerImageUrl = banner_image_url
        self.ItemReference = item_reference
        self.Title = title
        self.Type = type_
        self.Url = url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.NewsSite"
