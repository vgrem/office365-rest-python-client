from typing import Optional

from office365.runtime.client_value import ClientValue


class ProfileCoreProperties(ClientValue):
    def __init__(self, picture_url: Optional[str] = None, title: Optional[str] = None):
        self.PictureUrl = picture_url
        self.Title = title

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileCoreProperties"
