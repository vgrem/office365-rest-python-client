from office365.runtime.client_value import ClientValue


class SPOServicePrioritizationBillingPayload(ClientValue):
    def __init__(
        self,
        azure_region: str = None,
        azure_subscription: str = None,
        feature: str = None,
        friendly_name: str = None,
        identity_id: str = None,
        identity_type: str = None,
        policy_id: str = None,
        resource_group: str = None,
        scope: str = None,
        service: str = None,
        tags: str = None,
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
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationBillingPayload"
