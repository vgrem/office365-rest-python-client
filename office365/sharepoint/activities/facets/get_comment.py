from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.activities.identity import ActivityIdentity


@dataclass
class GetCommentFacet(ClientValue):
    """Args:
    assignees (list[ActivityIdentity]):
    comment_id (str):
    is_reply (bool):
    parent_author (ActivityIdentity): Gets or sets the parent author.
    parent_comment_id (str):
    participants (list[ActivityIdentity]):
    """

    assignees: ClientValueCollection[ActivityIdentity] = field(
        default_factory=lambda: ClientValueCollection(ActivityIdentity)
    )
    commentId: str | None = None
    isReply: bool | None = None
    parentAuthor: ActivityIdentity = field(default_factory=ActivityIdentity)
    parentCommentId: str | None = None
    participants: ClientValueCollection[ActivityIdentity] = field(
        default_factory=lambda: ClientValueCollection(ActivityIdentity)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.GetCommentFacet"
