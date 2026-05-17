from office365.runtime.client_value import ClientValue
from typing import Optional


class VivaHomeTitleRegion(ClientValue):
    def __init__(
        self,
        image_url=None,
        list_id: Optional[str] = None,
        site_id: Optional[str] = None,
        translate_x: Optional[float] = None,
        translate_y: Optional[float] = None,
        unique_id: Optional[str] = None,
        web_id: Optional[str] = None,
    ):
        """
        :param str image_url:
        """
        self.ImageUrl = image_url
        self.ListId = list_id
        self.SiteId = site_id
        self.TranslateX = translate_x
        self.TranslateY = translate_y
        self.UniqueId = unique_id
        self.WebId = web_id
