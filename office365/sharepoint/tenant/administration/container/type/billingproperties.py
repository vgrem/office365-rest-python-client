from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPContainerTypeBillingProperties(ClientValue):

    def __init__(
        self,
        azure_subscription_id: UUID = None,
        billing_policy_id: UUID = None,
        region: str = None,
        resource_group: str = None,
    ):
        self.AzureSubscriptionId = azure_subscription_id
        self.BillingPolicyId = billing_policy_id
        self.Region = region
        self.ResourceGroup = resource_group

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeBillingProperties"
