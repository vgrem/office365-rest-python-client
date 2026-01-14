from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.comments.client.identity import Identity
from office365.sharepoint.comments.contentanchor import ContentAnchor


class CommentInformation(ClientValue):
    def __init__(
        self,
        text: str = None,
        mentions: ClientValueCollection[Identity] = ClientValueCollection(Identity),
        content_anchor: ContentAnchor = ContentAnchor(),
    ):
        self.text = text
        self.mentions = mentions
        self.contentAnchor = content_anchor

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Comments.CommentInformation"
