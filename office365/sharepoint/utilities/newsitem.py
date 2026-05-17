from office365.runtime.client_value import ClientValue
from typing import Optional


class NewsItem(ClientValue):
    def __init__(
        self,
        backup_picture_url: Optional[str] = None,
        caption: Optional[str] = None,
        item_id: Optional[int] = None,
        picture_alt_text: Optional[str] = None,
        picture_url: Optional[str] = None,
        properties: Optional[str] = None,
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
