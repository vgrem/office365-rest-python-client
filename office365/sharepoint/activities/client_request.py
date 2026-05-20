from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.activities.facets.comment import CommentFacet
from office365.sharepoint.activities.facets.mention import MentionFacet
from office365.sharepoint.activities.facets.revision_set import RevisionSetFacet


@dataclass
class ActivityClientRequest(ClientValue):
    revisionSet: RevisionSetFacet = field(default_factory=RevisionSetFacet)
    comment: CommentFacet = field(default_factory=CommentFacet)
    contentAction: Optional[str] = None
    contentId: Optional[str] = None
    contentOrigin: Optional[str] = None
    created: Optional[str] = None
    id: Optional[UUID] = None
    mention: MentionFacet = field(default_factory=MentionFacet)
    navigationId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityClientRequest"
