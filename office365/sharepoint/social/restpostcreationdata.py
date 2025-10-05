from office365.runtime.client_value import ClientValue
from office365.sharepoint.social.posts.creation_data import SocialPostCreationData


class SocialRestPostCreationData(ClientValue):

    def __init__(
        self,
        id_: str = None,
        creation_data: SocialPostCreationData = SocialPostCreationData(),
    ):
        self.ID = id_
        self.creationData = creation_data

    @property
    def entity_type_name(self):
        return "SP.Social.SocialRestPostCreationData"
