from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.activities.activityclientidentity import (
    ActivityClientIdentity,
)


class CommentFacet(ClientValue):

    def __init__(
        self,
        comment_text: str = None,
        parent_author: ActivityClientIdentity = ActivityClientIdentity(),
        participants: ClientValueCollection[
            ActivityClientIdentity
        ] = ClientValueCollection(ActivityClientIdentity),
    ):
        self.commentText = comment_text
        self.parentAuthor = parent_author
        self.participants = participants

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.CommentFacet"
