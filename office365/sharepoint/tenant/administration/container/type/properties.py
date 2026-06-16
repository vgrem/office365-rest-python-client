from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.container.type.billingproperties import SPContainerTypeBillingProperties


@dataclass
class SPContainerTypeProperties(ClientValue):
    ApplicationRedirectUrl: str | None = None
    AzureSubscriptionId: UUID | None = None
    BillingProperties: SPContainerTypeBillingProperties = field(default_factory=SPContainerTypeBillingProperties)
    ContainerTypeId: UUID | None = None
    CreationDate: str | None = None
    DisplayName: str | None = None
    ExpiryDate: str | None = None
    IsBillingProfileRequired: bool | None = None
    IsGovernableByAdmin: bool | None = None
    IsGovernableByAdminNullable: int | None = None
    OwningAppId: UUID | None = None
    OwningTenantId: UUID | None = None
    Region: str | None = None
    ResourceGroup: str | None = None
    SPContainerTypeBillingClassification: int | None = None
    IsArchiveEnabled: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeProperties"
