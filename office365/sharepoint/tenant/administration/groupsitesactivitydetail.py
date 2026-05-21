from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class GroupSitesActivityDetail(ClientValue):
    GroupId: str | None = None
    LastActivityDate: datetime | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.GroupSitesActivityDetail"
