from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class GroupSitesActivityDetail(ClientValue):
    GroupId: str | None = None
    LastActivityDate: datetime | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.GroupSitesActivityDetail"
