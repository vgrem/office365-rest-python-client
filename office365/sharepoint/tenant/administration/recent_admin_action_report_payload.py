from office365.runtime.client_value import ClientValue


class RecentAdminActionReportPayload(ClientValue):
    """ """

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.RecentAdminActionReportPayload"
