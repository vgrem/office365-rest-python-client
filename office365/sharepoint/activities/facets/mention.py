from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.activities.activityclientidentity import (
    ActivityClientIdentity,
)


class MentionFacet(ClientValue):

    def __init__(
        self,
        comment_content_id: str = None,
        mentionees: ClientValueCollection[
            ActivityClientIdentity
        ] = ClientValueCollection(ActivityClientIdentity),
    ):
        self.commentContentId = comment_content_id
        self.mentionees = mentionees

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.MentionFacet"
