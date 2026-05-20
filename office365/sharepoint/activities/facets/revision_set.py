from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.activities.clientidentity import (
    ActivityClientIdentity,
)
from office365.sharepoint.activities.revision_info import RevisionInfo


@dataclass
class RevisionSetFacet(ClientValue):
    author: ActivityClientIdentity = field(default_factory=ActivityClientIdentity)
    revisions: ClientValueCollection[RevisionInfo] = field(default_factory=lambda: ClientValueCollection(RevisionInfo))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.RevisionSetFacet"
