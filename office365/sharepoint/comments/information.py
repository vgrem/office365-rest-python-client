from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.comments.client.identity import Identity


class CommentInformation(ClientValue):
    def __init__(
        self,
        text: str = None,
        mentions: ClientValueCollection[Identity] = ClientValueCollection(Identity),
    ):
        self.text = text
        self.mentions = mentions

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Comments.CommentInformation"
