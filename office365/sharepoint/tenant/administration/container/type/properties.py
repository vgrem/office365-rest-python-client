from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.container.type.billingproperties import (
    SPContainerTypeBillingProperties,
)


class SPContainerTypeProperties(ClientValue):

    def __init__(
        self,
        application_redirect_url: str = None,
        azure_subscription_id: UUID = None,
        billing_properties: SPContainerTypeBillingProperties = SPContainerTypeBillingProperties(),
        container_type_id: UUID = None,
        creation_date: str = None,
        display_name: str = None,
        expiry_date: str = None,
        is_billing_profile_required: bool = None,
        is_governable_by_admin: bool = None,
        is_governable_by_admin_nullable: int = None,
        owning_app_id: UUID = None,
        owning_tenant_id: UUID = None,
        region: str = None,
        resource_group: str = None,
        sp_container_type_billing_classification: int = None,
    ):
        self.ApplicationRedirectUrl = application_redirect_url
        self.AzureSubscriptionId = azure_subscription_id
        self.BillingProperties = billing_properties
        self.ContainerTypeId = container_type_id
        self.CreationDate = creation_date
        self.DisplayName = display_name
        self.ExpiryDate = expiry_date
        self.IsBillingProfileRequired = is_billing_profile_required
        self.IsGovernableByAdmin = is_governable_by_admin
        self.IsGovernableByAdminNullable = is_governable_by_admin_nullable
        self.OwningAppId = owning_app_id
        self.OwningTenantId = owning_tenant_id
        self.Region = region
        self.ResourceGroup = resource_group
        self.SPContainerTypeBillingClassification = (
            sp_container_type_billing_classification
        )

    @property
    def entity_type_name(self):
        return (
            "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeProperties"
        )
