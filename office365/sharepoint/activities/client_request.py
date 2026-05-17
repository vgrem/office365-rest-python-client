from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.activities.facets.comment import CommentFacet
from office365.sharepoint.activities.facets.mention import MentionFacet
from office365.sharepoint.activities.facets.revision_set import RevisionSetFacet


class ActivityClientRequest(ClientValue):
    def __init__(
        self,
        revision_set=RevisionSetFacet(),
        comment: CommentFacet = CommentFacet(),
        content_action: Optional[str] = None,
        content_id: Optional[str] = None,
        content_origin: Optional[str] = None,
        created: Optional[str] = None,
        id_: Optional[UUID] = None,
        mention: MentionFacet = MentionFacet(),
        navigation_id: Optional[str] = None,
    ):
        self.revisionSet = revision_set
        self.comment = comment
        self.contentAction = content_action
        self.contentId = content_id
        self.contentOrigin = content_origin
        self.created = created
        self.id = id_
        self.mention = mention
        self.navigationId = navigation_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityClientRequest"
