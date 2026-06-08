from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.collaboration.collaborativeonedriveuser import (
    CollaborativeOneDriveUser,
)
from office365.sharepoint.tenant.administration.collaboration.collaborativeusers import (
    CollaborativeUsers,
)


@dataclass
class CollaborationInsightsData(ClientValue):
    """Args:
        last_report_date (str):
        collaborative_users (list[CollaborativeUsers]):
    """

    collaborativeUsers: ClientValueCollection[CollaborativeUsers] = field(
        default_factory=lambda: ClientValueCollection(CollaborativeUsers)
    )
    lastReportDate: str | None = None
    collaborativeOneDriveUsers: ClientValueCollection[CollaborativeOneDriveUser] = field(
        default_factory=lambda: ClientValueCollection(CollaborativeOneDriveUser)
    )

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.CollaborationInsightsData"
