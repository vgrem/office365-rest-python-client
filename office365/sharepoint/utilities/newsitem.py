from office365.runtime.client_value import ClientValue


class NewsItem(ClientValue):

    def __init__(
        self,
        backup_picture_url: str = None,
        caption: str = None,
        item_id: int = None,
        picture_alt_text: str = None,
        picture_url: str = None,
        properties: str = None,
    ):
        self.backupPictureUrl = backup_picture_url
        self.caption = caption
        self.itemId = item_id
        self.pictureAltText = picture_alt_text
        self.pictureUrl = picture_url
        self.properties = properties

    @property
    def entity_type_name(self):
        return "SP.Utilities.NewsItem"
