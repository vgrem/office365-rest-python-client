from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.comments.client.identity import Identity
from office365.sharepoint.comments.contentanchor import ContentAnchor


@value
class CommentInformation(ClientValue):
    text: Optional[str] = None
    mentions: ClientValueCollection[Identity] = field(default_factory=lambda: ClientValueCollection(Identity))
    contentAnchor: ContentAnchor = field(default_factory=ContentAnchor)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Comments.CommentInformation"
