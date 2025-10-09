from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.contentmanagementassessmentpolicyreportdetails import (
    ContentManagementAssessmentPolicyReportDetails as CMAPolicyDetails,
)
from office365.sharepoint.tenant.administration.reports.sitepermissionsdetails import (
    SitePermissionsReportDetails,
)


class ContentManagementAssessmentResults(ClientValue):

    def __init__(
        self,
        last_updated_time: datetime = None,
        requested_time: datetime = None,
        site_lifecycle_management_impacted_file_url: str = None,
        site_lifecycle_management_policy_execution_id: int = None,
        site_lifecycle_management_policy_id: str = None,
        site_lifecycle_management_policy_last_updated_time: datetime = None,
        site_lifecycle_management_policy_result_state: int = None,
        site_lifecycle_management_report_details: CMAPolicyDetails = CMAPolicyDetails(),
        site_permissions_report_definition_id: str = None,
        site_permissions_report_details: SitePermissionsReportDetails = SitePermissionsReportDetails(),
        site_permissions_report_id: str = None,
        site_permissions_report_last_updated_time: datetime = None,
        site_permissions_report_queued_time: datetime = None,
        site_permissions_report_result_state: int = None,
        total_count_of_sites_in_tenant: str = None,
    ):
        self.lastUpdatedTime = last_updated_time
        self.requestedTime = requested_time
        self.siteLifecycleManagementImpactedFileUrl = (
            site_lifecycle_management_impacted_file_url
        )
        self.siteLifecycleManagementPolicyExecutionId = (
            site_lifecycle_management_policy_execution_id
        )
        self.siteLifecycleManagementPolicyId = site_lifecycle_management_policy_id
        self.siteLifecycleManagementPolicyLastUpdatedTime = (
            site_lifecycle_management_policy_last_updated_time
        )
        self.siteLifecycleManagementPolicyResultState = (
            site_lifecycle_management_policy_result_state
        )
        self.siteLifecycleManagementReportDetails = (
            site_lifecycle_management_report_details
        )
        self.sitePermissionsReportDefinitionId = site_permissions_report_definition_id
        self.sitePermissionsReportDetails = site_permissions_report_details
        self.sitePermissionsReportId = site_permissions_report_id
        self.sitePermissionsReportLastUpdatedTime = (
            site_permissions_report_last_updated_time
        )
        self.sitePermissionsReportQueuedTime = site_permissions_report_queued_time
        self.sitePermissionsReportResultState = site_permissions_report_result_state
        self.totalCountOfSitesInTenant = total_count_of_sites_in_tenant

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.ContentManagementAssessmentResults"
