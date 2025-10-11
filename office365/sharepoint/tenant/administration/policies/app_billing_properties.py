from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPOAppBillingProperties(ClientValue):
    """ """

    def __init__(
        self,
        application_id=None,
        azure_region=None,
        is_activated=None,
        resource_group: str = None,
        subscription_id: UUID = None,
        subscription_state: str = None,
        usage_charges: str = None,
    ):
        """
        :param str application_id: The application ID.
        :param str azure_region: The Azure region.
        :param bool is_activated:
        """
        self.ApplicationId = application_id
        self.AzureRegion = azure_region
        self.IsActivated = is_activated
        self.ResourceGroup = resource_group
        self.SubscriptionId = subscription_id
        self.SubscriptionState = subscription_state
        self.UsageCharges = usage_charges

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOAppBillingProperties"
