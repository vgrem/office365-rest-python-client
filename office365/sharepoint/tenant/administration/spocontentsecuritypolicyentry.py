from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPOContentSecurityPolicyEntry(ClientValue):
    Manual: bool | None = None
    Modified: datetime | None = None
    Source: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOContentSecurityPolicyEntry"
