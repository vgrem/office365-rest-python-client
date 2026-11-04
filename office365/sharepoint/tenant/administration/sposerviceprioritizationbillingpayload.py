from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPOServicePrioritizationBillingPayload(ClientValue):
    AzureRegion: str | None = None
    AzureSubscription: str | None = None
    Feature: str | None = None
    FriendlyName: str | None = None
    IdentityId: str | None = None
    IdentityType: str | None = None
    PolicyId: str | None = None
    ResourceGroup: str | None = None
    Scope: str | None = None
    Service: str | None = None
    Tags: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationBillingPayload"
