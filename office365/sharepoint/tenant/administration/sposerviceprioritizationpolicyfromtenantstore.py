from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPOServicePrioritizationPolicyFromTenantStore(ClientValue):

    def __init__(
        self,
        azure_region: str = None,
        azure_subscription_id: UUID = None,
        friendly_name: str = None,
        policy_id: UUID = None,
        resource_group: str = None,
    ):
        self.AzureRegion = azure_region
        self.AzureSubscriptionId = azure_subscription_id
        self.FriendlyName = friendly_name
        self.PolicyId = policy_id
        self.ResourceGroup = resource_group

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationPolicyFromTenantStore"
