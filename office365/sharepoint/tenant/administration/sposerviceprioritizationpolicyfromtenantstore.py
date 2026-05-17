from uuid import UUID

from office365.runtime.client_value import ClientValue
from typing import Optional


class SPOServicePrioritizationPolicyFromTenantStore(ClientValue):
    def __init__(
        self,
        azure_region: Optional[str] = None,
        azure_subscription_id: Optional[UUID] = None,
        friendly_name: Optional[str] = None,
        policy_id: Optional[UUID] = None,
        resource_group: Optional[str] = None,
    ):
        self.AzureRegion = azure_region
        self.AzureSubscriptionId = azure_subscription_id
        self.FriendlyName = friendly_name
        self.PolicyId = policy_id
        self.ResourceGroup = resource_group

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationPolicyFromTenantStore"
