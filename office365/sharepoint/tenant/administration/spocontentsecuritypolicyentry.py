from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class SPOContentSecurityPolicyEntry(ClientValue):
    Manual: bool | None = None
    Modified: datetime | None = None
    Source: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOContentSecurityPolicyEntry"
