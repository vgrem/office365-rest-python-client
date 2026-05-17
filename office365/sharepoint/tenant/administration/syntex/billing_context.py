from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class SyntexBillingContext(ClientValue):
    def __init__(
        self,
        activation_status: Optional[int] = None,
        azure_resource_id: Optional[str] = None,
        azure_subscription_state: Optional[int] = None,
        enabled_features: Optional[int] = None,
        location: Optional[str] = None,
        updated: Optional[datetime] = None,
    ):
        self.ActivationStatus = activation_status
        self.AzureResourceId = azure_resource_id
        self.AzureSubscriptionState = azure_subscription_state
        self.EnabledFeatures = enabled_features
        self.Location = location
        self.Updated = updated

    ""

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexBillingContext"
