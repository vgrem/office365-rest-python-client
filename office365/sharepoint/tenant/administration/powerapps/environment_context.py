from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class PowerAppsEnvironmentContext(ClientValue):
    DataverseInstanceUrl: str | None = None
    DisplayName: str | None = None
    IsTestEnvironment: bool | None = None
    LastGetEnvironmentError: str | None = None
    Name: str | None = None
    UpdatedUTC: datetime | None = field(default_factory=lambda: datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.PowerAppsEnvironmentContext"
