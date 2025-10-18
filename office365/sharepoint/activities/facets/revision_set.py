from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.activities.clientidentity import (
    ActivityClientIdentity,
)
from office365.sharepoint.activities.revision_info import RevisionInfo


class RevisionSetFacet(ClientValue):

    def __init__(
        self,
        author: ActivityClientIdentity = ActivityClientIdentity(),
        revisions: ClientValueCollection[RevisionInfo] = ClientValueCollection(RevisionInfo),
    ):
        self.author = author
        self.revisions = revisions

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.RevisionSetFacet"
