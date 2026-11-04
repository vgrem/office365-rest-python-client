from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SyntexBillingContext(ClientValue):
    ActivationStatus: int | None = None
    AzureResourceId: str | None = None
    AzureSubscriptionState: int | None = None
    EnabledFeatures: int | None = None
    Location: str | None = None
    Updated: datetime | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexBillingContext"
