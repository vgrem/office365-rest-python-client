from office365.runtime.client_value import ClientValue


class VivaHomeTitleRegion(ClientValue):
    def __init__(
        self,
        image_url=None,
        list_id: str = None,
        site_id: str = None,
        translate_x: float = None,
        translate_y: float = None,
        unique_id: str = None,
        web_id: str = None,
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
