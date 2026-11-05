from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TenantDefaultTimeZoneId(ClientValue):
    IsReadOnly: bool | None = None
    Value: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.TenantDefaultTimeZoneId"
