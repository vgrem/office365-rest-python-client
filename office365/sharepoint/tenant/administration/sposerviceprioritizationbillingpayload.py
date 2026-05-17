from office365.runtime.client_value import ClientValue
from typing import Optional


class SPOServicePrioritizationBillingPayload(ClientValue):
    def __init__(
        self,
        azure_region: Optional[str] = None,
        azure_subscription: Optional[str] = None,
        feature: Optional[str] = None,
        friendly_name: Optional[str] = None,
        identity_id: Optional[str] = None,
        identity_type: Optional[str] = None,
        policy_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        scope: Optional[str] = None,
        service: Optional[str] = None,
        tags: Optional[str] = None,
    ):
        self.AzureRegion = azure_region
        self.AzureSubscription = azure_subscription
        self.Feature = feature
        self.FriendlyName = friendly_name
        self.IdentityId = identity_id
        self.IdentityType = identity_type
        self.PolicyId = policy_id
        self.ResourceGroup = resource_group
        self.Scope = scope
        self.Service = service
        self.Tags = tags

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationBillingPayload"
