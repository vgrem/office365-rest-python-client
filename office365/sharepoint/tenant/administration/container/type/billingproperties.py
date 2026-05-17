from uuid import UUID

from office365.runtime.client_value import ClientValue
from typing import Optional


class SPContainerTypeBillingProperties(ClientValue):
    def __init__(
        self,
        azure_subscription_id: Optional[UUID] = None,
        billing_policy_id: Optional[UUID] = None,
        region: Optional[str] = None,
        resource_group: Optional[str] = None,
    ):
        self.AzureSubscriptionId = azure_subscription_id
        self.BillingPolicyId = billing_policy_id
        self.Region = region
        self.ResourceGroup = resource_group

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeBillingProperties"
