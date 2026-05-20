from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.activities.clientidentity import (
    ActivityClientIdentity,
)


@dataclass
class CommentFacet(ClientValue):
    commentText: Optional[str] = None
    parentAuthor: ActivityClientIdentity = field(default_factory=ActivityClientIdentity)
    participants: ClientValueCollection[ActivityClientIdentity] = field(
        default_factory=lambda: ClientValueCollection(ActivityClientIdentity)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.CommentFacet"
