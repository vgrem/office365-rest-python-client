from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPContainerTypeStatus(ClientValue):

    def __init__(
        self,
        container_type_id: UUID = None,
        is_active_billing_profile: bool = None,
        is_archivable: bool = None,
    ):
        self.ContainerTypeId = container_type_id
        self.IsActiveBillingProfile = is_active_billing_profile
        self.IsArchivable = is_archivable

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeStatus"
