from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPOServicePrioritizationPolicyFromTenantStore(ClientValue):
    AzureRegion: str | None = None
    AzureSubscriptionId: UUID | None = None
    FriendlyName: str | None = None
    PolicyId: UUID | None = None
    ResourceGroup: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationPolicyFromTenantStore"
