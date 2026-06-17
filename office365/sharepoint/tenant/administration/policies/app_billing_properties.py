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

    ResourceGroup: str | None = None
    SubscriptionId: UUID | None = None
    SubscriptionState: str | None = None
    UsageCharges: str | None = None
    ApplicationId: UUID | None = None
    AzureRegion: str | None = None
    IsActivated: bool | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOAppBillingProperties"
