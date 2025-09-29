from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.social.microfeed.user_posts import MicrofeedUserPosts


class MicrofeedUserPostCollection(ClientValue):

    def __init__(
        self,
        items: ClientValueCollection[MicrofeedUserPosts] = ClientValueCollection(
            MicrofeedUserPosts
        ),
    ):
        self.Items = items
