from office365.runtime.client_value import ClientValue


class SPOTenantVersionPolicyImpact(ClientValue):
    TrimCount: int | None = None
    TrimStorageGB: float | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOTenantVersionPolicyImpact"
