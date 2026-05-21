from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.activities.identity import ActivityIdentity


@dataclass
class GetCommentFacet(ClientValue):
    """
    :param list[ActivityIdentity] assignees:
    :param str comment_id:
    :param bool is_reply:
    :param ActivityIdentity parent_author: Gets or sets the parent author.
    :param str parent_comment_id:
    :param list[ActivityIdentity] participants:
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
