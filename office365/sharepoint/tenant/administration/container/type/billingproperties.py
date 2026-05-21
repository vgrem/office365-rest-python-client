from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPContainerTypeBillingProperties(ClientValue):
    AzureSubscriptionId: UUID | None = None
    BillingPolicyId: UUID | None = None
    Region: str | None = None
    ResourceGroup: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeBillingProperties"
