from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


class SPDataGovernanceInsightResponse(ClientValue):

    def __init__(
        self,
        count_of_sites_in_report: int = None,
        count_of_sites_in_report_user_permissions: int = None,
        count_of_sites_in_tenant: int = None,
        count_of_sites_in_tenant_user_permissions: int = None,
        created_date_time: str = None,
        eeeu_type: str = None,
        invalid_user_entries: StringCollection = StringCollection(),
        label_id: UUID = None,
        label_name: str = None,
        privacy_eeeu: StringCollection = StringCollection(),
        privacy_site_permissions: str = None,
        report_end_time_eeeu: str = None,
        report_end_time_sharing_link: str = None,
        report_entity: str = None,
        report_format: str = None,
        report_id: UUID = None,
        report_name_eeeu: str = None,
        report_name_site_permissions: str = None,
        report_name_user_permissions: str = None,
        report_start_time_eeeu: str = None,
        report_start_time_sharing_link: str = None,
        report_type: str = None,
        sensitivity_eeeu: StringCollection = StringCollection(),
        sensitivity_site_permissions: StringCollection = StringCollection(),
        sharing_link_type: str = None,
        sites_found_eeeu: int = None,
        sites_found_sharing_link: int = None,
        status: str = None,
        templates_eeeu: StringCollection = StringCollection(),
        templates_site_permissions: StringCollection = None,
        triggered_date_time: str = None,
        user_email_list: StringCollection = StringCollection(),
        user_id: UUID = None,
        user_id_list: GuidCollection = GuidCollection(),
        user_limit: int = None,
        variation: str = None,
        version: str = None,
        workload: str = None,
    ):
        self.CountOfSitesInReport = count_of_sites_in_report
        self.CountOfSitesInReportUserPermissions = (
            count_of_sites_in_report_user_permissions
        )
        self.CountOfSitesInTenant = count_of_sites_in_tenant
        self.CountOfSitesInTenantUserPermissions = (
            count_of_sites_in_tenant_user_permissions
        )
        self.CreatedDateTime = created_date_time
        self.EEEUType = eeeu_type
        self.InvalidUserEntries = invalid_user_entries
        self.LabelId = label_id
        self.LabelName = label_name
        self.PrivacyEEEU = privacy_eeeu
        self.PrivacySitePermissions = privacy_site_permissions
        self.ReportEndTimeEEEU = report_end_time_eeeu
        self.ReportEndTimeSharingLink = report_end_time_sharing_link
        self.ReportEntity = report_entity
        self.ReportFormat = report_format
        self.ReportId = report_id
        self.ReportNameEEEU = report_name_eeeu
        self.ReportNameSitePermissions = report_name_site_permissions
        self.ReportNameUserPermissions = report_name_user_permissions
        self.ReportStartTimeEEEU = report_start_time_eeeu
        self.ReportStartTimeSharingLink = report_start_time_sharing_link
        self.ReportType = report_type
        self.SensitivityEEEU = sensitivity_eeeu
        self.SensitivitySitePermissions = sensitivity_site_permissions
        self.SharingLinkType = sharing_link_type
        self.SitesFoundEEEU = sites_found_eeeu
        self.SitesFoundSharingLink = sites_found_sharing_link
        self.Status = status
        self.TemplatesEEEU = templates_eeeu
        self.TemplatesSitePermissions = templates_site_permissions
        self.TriggeredDateTime = triggered_date_time
        self.UserEmailList = user_email_list
        self.UserID = user_id
        self.UserIDList = user_id_list
        self.UserLimit = user_limit
        self.Variation = variation
        self.Version = version
        self.Workload = workload

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceInsightResponse"
