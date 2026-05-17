from typing import Optional

from office365.runtime.client_value import ClientValue


class SPDataGovernanceInsightExportedReport(ClientValue):
    def __init__(
        self,
        created_date_time: Optional[str] = None,
        label_name: Optional[str] = None,
        report_content: Optional[str] = None,
        report_entity: Optional[str] = None,
        report_name_eeeu: Optional[str] = None,
        report_name_site_permissions: Optional[str] = None,
        report_name_user_permissions: Optional[str] = None,
        sharing_link_type: Optional[str] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceInsightExportedReport"
