from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPOAppBillingProperties(ClientValue):
    """Args:
    application_id (str): The application ID.
    azure_region (str): The Azure region.
    is_activated (bool):
    """

    ApplicationId = None
    AzureRegion = None
    IsActivated = None
    ResourceGroup: str | None = None
    SubscriptionId: UUID | None = None
    SubscriptionState: str | None = None
    UsageCharges: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOAppBillingProperties"
