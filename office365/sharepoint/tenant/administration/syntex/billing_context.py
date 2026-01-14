from datetime import datetime

from office365.runtime.client_value import ClientValue


class SyntexBillingContext(ClientValue):
    def __init__(
        self,
        activation_status: int = None,
        azure_resource_id: str = None,
        azure_subscription_state: int = None,
        enabled_features: int = None,
        location: str = None,
        updated: datetime = None,
    ):
        self.ActivationStatus = activation_status
        self.AzureResourceId = azure_resource_id
        self.AzureSubscriptionState = azure_subscription_state
        self.EnabledFeatures = enabled_features
        self.Location = location
        self.Updated = updated

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexBillingContext"
