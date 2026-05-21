from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ModifiedProperty(ClientValue):
    Name: str | None = None
    NewValue: str | None = None
    OldValue: str | None = None
    displayName: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.ModifiedProperty"
