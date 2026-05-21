from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPOAppBillingProperties(ClientValue):
    """:param str application_id: The application ID.
    :param str azure_region: The Azure region.
    :param bool is_activated:"""

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
