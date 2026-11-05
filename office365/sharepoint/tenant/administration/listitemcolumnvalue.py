from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TenantAdminListItemColumnValue(ClientValue):
    columnName: str | None = None
    columnValue: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminListItemColumnValue"
