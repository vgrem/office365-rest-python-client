from office365.runtime.client_value import ClientValue


class ProfileCoreProperties(ClientValue):
    def __init__(self, picture_url: str = None, title: str = None):
        self.PictureUrl = picture_url
        self.Title = title

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileCoreProperties"
