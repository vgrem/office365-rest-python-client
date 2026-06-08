from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.activities.identity import ActivityIdentity


@dataclass
class SharingFacet(ClientValue):
    """Args:
        recipients (list[ActivityIdentity]):
        sharing_type (str):
    """

    recipients: ClientValueCollection[ActivityIdentity] = field(
        default_factory=lambda: ClientValueCollection(ActivityIdentity)
    )
    sharingType: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.SharingFacet"
