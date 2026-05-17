from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


class SPDataGovernanceInsightResponse(ClientValue):
    def __init__(
        self,
        count_of_sites_in_report: Optional[int] = None,
        count_of_sites_in_report_user_permissions: Optional[int] = None,
        count_of_sites_in_tenant: Optional[int] = None,
        count_of_sites_in_tenant_user_permissions: Optional[int] = None,
        created_date_time: Optional[str] = None,
        eeeu_type: Optional[str] = None,
        invalid_user_entries: StringCollection = StringCollection(),
        label_id: Optional[UUID] = None,
        label_name: Optional[str] = None,
        privacy_eeeu: StringCollection = StringCollection(),
        privacy_site_permissions: Optional[str] = None,
        report_end_time_eeeu: Optional[str] = None,
        report_end_time_sharing_link: Optional[str] = None,
        report_entity: Optional[str] = None,
        report_format: Optional[str] = None,
        report_id: Optional[UUID] = None,
        report_name_eeeu: Optional[str] = None,
        report_name_site_permissions: Optional[str] = None,
        report_name_user_permissions: Optional[str] = None,
        report_start_time_eeeu: Optional[str] = None,
        report_start_time_sharing_link: Optional[str] = None,
        report_type: Optional[str] = None,
        sensitivity_eeeu: StringCollection = StringCollection(),
        sensitivity_site_permissions: StringCollection = StringCollection(),
        sharing_link_type: Optional[str] = None,
        sites_found_eeeu: Optional[int] = None,
        sites_found_sharing_link: Optional[int] = None,
        status: Optional[str] = None,
        templates_eeeu: StringCollection = StringCollection(),
        templates_site_permissions: Optional[StringCollection] = None,
        triggered_date_time: Optional[str] = None,
        user_email_list: StringCollection = StringCollection(),
        user_id: Optional[UUID] = None,
        user_id_list: GuidCollection = GuidCollection(),
        user_limit: Optional[int] = None,
        variation: Optional[str] = None,
        version: Optional[str] = None,
        workload: Optional[str] = None,
    ):
        self.CountOfSitesInReport = count_of_sites_in_report
        self.CountOfSitesInReportUserPermissions = count_of_sites_in_report_user_permissions
        self.CountOfSitesInTenant = count_of_sites_in_tenant
        self.CountOfSitesInTenantUserPermissions = count_of_sites_in_tenant_user_permissions
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceInsightResponse"
