from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.viva.dashboard.carddetails import DashboardCardDetails


@dataclass
class DashboardContent(ClientValue):
    DashboardCardDetails: ClientValueCollection[DashboardCardDetails] = field(
        default_factory=lambda: ClientValueCollection(DashboardCardDetails)
    )
    DashboardFormFactor: Optional[str] = None
    DashboardId: Optional[str] = None
    LastModifiedDate: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.DashboardContent"
