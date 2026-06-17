from office365.runtime.client_value import ClientValue


class SPDataGovernanceOptInParameters(ClientValue):
    OptInStatus: bool | None = None
    ReportEntity: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceOptInParameters"
