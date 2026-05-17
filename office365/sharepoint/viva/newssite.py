from office365.runtime.client_value import ClientValue
from office365.sharepoint.news.itemreference import NewsItemReference as ItemReference
from typing import Optional


class NewsSite(ClientValue):
    def __init__(
        self,
        acronym: Optional[str] = None,
        banner_color: Optional[str] = None,
        banner_image_url: Optional[str] = None,
        item_reference: ItemReference = ItemReference(),
        title: Optional[str] = None,
        type_: Optional[str] = None,
        url: Optional[str] = None,
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
