from office365.runtime.client_value import ClientValue


class SPDataGovernanceInsightExportedReport(ClientValue):
    def __init__(
        self,
        created_date_time: str = None,
        label_name: str = None,
        report_content: str = None,
        report_entity: str = None,
        report_name_eeeu: str = None,
        report_name_site_permissions: str = None,
        report_name_user_permissions: str = None,
        sharing_link_type: str = None,
    ):
        self.CreatedDateTime = created_date_time
        self.LabelName = label_name
        self.ReportContent = report_content
        self.ReportEntity = report_entity
        self.ReportNameEEEU = report_name_eeeu
        self.ReportNameSitePermissions = report_name_site_permissions
        self.ReportNameUserPermissions = report_name_user_permissions
        self.SharingLinkType = sharing_link_type

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceInsightExportedReport"
