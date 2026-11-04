from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class TenantAdminRansomwareEventsOverview(ClientValue):
    activeEventsCount: int | None = None
    openEventsCount: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareEventsOverview"
