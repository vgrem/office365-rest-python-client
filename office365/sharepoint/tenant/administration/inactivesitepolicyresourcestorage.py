from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.fields.lookup_value import FieldLookupValue


@dataclass
class InactiveSitePolicyResourceStorage(ClientValue):
    createdOn: datetime | None = None
    lastScopedOn: datetime | None = None
    lastTransitionedOn: datetime | None = None
    lookupSiteId: FieldLookupValue = field(default_factory=FieldLookupValue)
    notificationData: str | None = None
    notificationStatus: int | None = None
    resourceId: str | None = None
    resourceState: int | None = None
    resourceStateTransitionData: str | None = None
    resourceType: int | None = None
    updatedOn: datetime | None = None
    userResponses: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.InactiveSitePolicyResourceStorage"
