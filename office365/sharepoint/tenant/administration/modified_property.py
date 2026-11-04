from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ModifiedProperty(ClientValue):
    Name: str | None = None
    NewValue: str | None = None
    OldValue: str | None = None
    displayName: str | None = None
    newValue: str | None = None
    oldValue: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.ModifiedProperty"
