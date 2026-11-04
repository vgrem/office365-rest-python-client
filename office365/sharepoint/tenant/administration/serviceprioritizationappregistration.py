from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPOServicePrioritizationAppRegistration(ClientValue):
    AppId: str | None = None
    Enabled: bool | None = None
    PolicyId: str | None = None
    QuotaMultiplier: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationAppRegistration"
