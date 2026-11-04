from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PowerAppsEnvironment(ClientValue):
    AllocatedAICredits: float | None = None
    DisplayName: str | None = None
    IsDefault: bool | None = None
    Name: str | None = None
    PurchasedAICredits: float | None = None

    def __str__(self):
        return self.DisplayName or self.entity_type_name

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.PowerAppsEnvironment"
