from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class ValueDisplayNameSettings(ClientValue):
    displayName: str | None = None
    id: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.ValueDisplayNameSettings"
