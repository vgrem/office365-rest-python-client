from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional, Union

from office365.directory.authentication.methods.root import AuthenticationMethodsRoot
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.partners.partners import Partners
from office365.permissions import require_permission
from office365.reports.internal.queries.create_report_query import create_report_query
from office365.reports.print_usage_by_printer import PrintUsageByPrinter
from office365.reports.print_usage_by_user import PrintUsageByUser
from office365.reports.quotas import REPORT_QUOTAS
from office365.reports.report_export import (
    ReportExportResult,
    ReportTarget,
    download_report,
    download_report_async,
)
from office365.reports.report_result import ReportResult
from office365.reports.security.root import SecurityReportsRoot
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.limits import limit
from office365.runtime.operations import ProgressCallback
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.transport.base import DEFAULT_STREAM_CHUNK_SIZE
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.print.archived_print_job import ArchivedPrintJob
    from office365.reports.relying_party_detailed_summary import RelyingPartyDetailedSummary
    from office365.reports.report import Report


@limit(*REPORT_QUOTAS)
class ReportRoot(Entity):
    """Represents a container for Azure Active Directory (Azure AD) reporting resources."""

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def download_report(
        self,
        report_name: str,
        target: ReportTarget,
        period: Optional[str] = None,
        *,
        chunk_size: int = DEFAULT_STREAM_CHUNK_SIZE,
        progress: Optional[ProgressCallback] = None,
    ) -> ReportExportResult:
        """Stream a usage report to ``target`` without buffering it in memory.

        The Graph reports API answers with a ``302`` to a pre-authenticated
        download URL; this helper follows it through the normal transport and
        writes the CSV (or JSON) to a path or an already-open binary stream,
        returning the bytes written and the server's file name.

        Args:
            report_name: The Graph function name, e.g.
                ``"getTeamsUserActivityUserDetail"``. ``*UserDetail`` reports
                also need ``period``.
            target: A filesystem path or a writable binary stream.
            period: Aggregation period (``D7``, ``D30``, ``D90``, ``D180``).
            chunk_size: Number of bytes read per chunk.
            progress: Optional ``ProgressCallback`` invoked per chunk.
        """
        return download_report(self, report_name, target, period, chunk_size=chunk_size, progress=progress)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    async def download_report_async(
        self,
        report_name: str,
        target: ReportTarget,
        period: Optional[str] = None,
        *,
        chunk_size: int = DEFAULT_STREAM_CHUNK_SIZE,
        progress: Optional[ProgressCallback] = None,
    ) -> ReportExportResult:
        """Async twin of :meth:`download_report` that never blocks the loop."""
        return await download_report_async(self, report_name, target, period, chunk_size=chunk_size, progress=progress)

    @require_permission(
        delegated=["DeviceManagementConfiguration.Read.All"], application=["DeviceManagementConfiguration.Read.All"]
    )
    def device_configuration_device_activity(self) -> ReportResult:
        """
        Metadata for the device configuration device activity report
        """
        return_type = ReportResult(self.context)
        qry = FunctionQuery(self, "deviceConfigurationDeviceActivity", None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=["DeviceManagementConfiguration.Read.All"], application=["DeviceManagementConfiguration.Read.All"]
    )
    def device_configuration_user_activity(self) -> ReportResult:
        """
        Metadata for the device configuration user activity report
        """
        return_type = ReportResult(self.context)
        qry = FunctionQuery(self, "deviceConfigurationUserActivity", None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=["DeviceManagementManagedDevices.Read.All"], application=["DeviceManagementManagedDevices.Read.All"]
    )
    def managed_device_enrollment_failure_details(self) -> ReportResult:
        """ """
        return_type = ReportResult(self.context)
        qry = FunctionQuery(self, "managedDeviceEnrollmentFailureDetails", None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=["Reports.Read.All"],
        application=["Reports.Read.All"],
    )
    def managed_device_enrollment_top_failures(self, period: Optional[str] = None) -> ReportResult:
        """
        Note: The Microsoft Graph API for Intune requires an active Intune license for the tenant.
        """
        return_type = ReportResult(self.context)
        qry = FunctionQuery(self, "managedDeviceEnrollmentTopFailures", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_email_activity_counts(self, period: str) -> ReportResult:
        """Enables you to understand the trends of email activity (like how many were sent, read, and received)
        in your organization.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values for
              {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return_type = ReportResult(self.context)
        qry = FunctionQuery(self, "getEmailActivityCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_email_activity_user_counts(self, period: str):
        """Enables you to understand trends on the number of unique users who are performing email activities
        like send, read, and receive.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getEmailActivityUserCounts", period)

    def get_email_activity_user_detail(self, period: str) -> ReportResult:
        """Get details about email activity users have performed.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getEmailActivityUserDetail", period)

    def get_email_app_usage_apps_user_counts(self, period: str) -> ReportResult:
        """Get the count of unique users per email app.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getEmailAppUsageAppsUserCounts", period)

    def get_email_app_usage_user_counts(self, period) -> ReportResult:
        """Get the count of unique users that connected to Exchange Online using any email app.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getEmailAppUsageUserCounts", period)

    def get_email_app_usage_user_detail(self, period: str) -> ReportResult:
        """Get details about which activities users performed on the various email apps.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getEmailAppUsageUserDetail", period)

    def get_mailbox_usage_storage(self, period: str) -> ReportResult:
        """Get the amount of storage used in your organization.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getMailboxUsageStorage", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_m365_app_user_counts(self, period: Optional[str] = None) -> ReportResult:
        """
        Get a report that provides the trend in the number of active users for each app (Outlook, Word, Excel,
        PowerPoint, OneNote, and Teams) in your organization.
        """
        return_type = ReportResult(self.context)
        qry = FunctionQuery(self, "getM365AppUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=["Reports.Read.All"],
        application=["Reports.Read.All"],
    )
    def get_m365_app_user_detail(self, period_or_date: Optional[Union[date, str]] = None) -> ReportResult:
        """
        Get a report that provides the details about which apps and platforms users have used.
        """
        return_type = ReportResult(self.context)
        qry = FunctionQuery(self, "getM365AppUserDetail", {"period": period_or_date}, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_office365_activation_counts(self):
        """Get the count of Microsoft 365 activations on desktops and devices."""
        return create_report_query(self, "getOffice365ActivationCounts")

    def get_office365_activations_user_counts(self) -> ReportResult:
        """Get the count of Microsoft 365 activations on desktops and devices."""
        return create_report_query(self, "getOffice365ActivationsUserCounts")

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_onedrive_activity_file_counts(self, period: str) -> ReportResult:
        """Get the number of unique, licensed users that performed file interactions against any OneDrive account.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getOneDriveActivityFileCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_onedrive_activity_user_counts(self, period: str) -> ReportResult:
        """Get the trend in the number of active OneDrive users.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getOneDriveActivityUserCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_onedrive_activity_user_detail(self, period: str):
        """Get details about OneDrive activity by user.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getOneDriveActivityUserDetail", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_onedrive_usage_file_counts(self, period: str) -> ReportResult:
        """Get the total number of files across all sites and how many are active files. A file is considered active
        if it has been saved, synced, modified, or shared within the specified time period.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getOneDriveUsageFileCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_onedrive_usage_storage(self, period) -> ReportResult:
        """Get the trend on the amount of storage you are using in OneDrive for Business.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getOneDriveUsageStorage", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_mailbox_usage_detail(self, period) -> ReportResult:
        """Get details about mailbox usage.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getMailboxUsageDetail", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_mailbox_usage_mailbox_counts(self, period: str) -> ReportResult:
        """Get the total number of user mailboxes in your organization and how many are active each day of the reporting
        period. A mailbox is considered active if the user sent or read any email.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getMailboxUsageMailboxCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_mailbox_usage_quota_status_mailbox_counts(self, period: str):
        """Args:
        period (str): Specifies the length of time over which the report is aggregated. The supported values
          for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
          the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getMailboxUsageQuotaStatusMailboxCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_sharepoint_activity_pages(self, period: str):
        """Get the number of unique pages visited by users.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
            for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
            the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getSharePointActivityPages", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_teams_user_activity_user_counts(self, period: str) -> ReportResult:
        """Get the number of Microsoft Teams users by activity type. The activity types are number
        of teams chat messages, private chat messages, calls, or meetings.

        Args:
            period (str): Specifies the length of time over which the report is aggregated.
        """
        return create_report_query(self, "getTeamsUserActivityUserCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_sharepoint_activity_user_counts(self, period: str):
        """Get the trend in the number of active users. A user is considered active if he or she has executed a
        file activity (save, sync, modify, or share) or visited a page within the specified time period.

        Args:
            period (str): Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the
            format Dn where n represents the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getSharePointActivityUserCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_sharepoint_activity_user_detail(self, period: str):
        """Get details about SharePoint activity by user.

        Args:
            period (str): Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the
            format Dn where n represents the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getSharePointActivityUserDetail", period)

    def get_sharepoint_site_usage_detail(self, period: str) -> ReportResult:
        """Get details about SharePoint site usage.

        Args:
            period (str): Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getSharePointSiteUsageDetail", period)

    def get_sharepoint_site_usage_site_counts(self, period: str) -> ReportResult:
        """Get the trend of total and active site count during the reporting period.

        Args:
            period (str): Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getSharePointSiteUsageSiteCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_teams_team_counts(self, period: str) -> ReportResult:
        """Get the number of teams of a particular type in an instance of Microsoft Teams.

        Args:
            period (str): Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the
            format Dn where n represents the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getTeamsTeamCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_teams_user_activity_counts(self, period: str) -> ReportResult:
        """
        Get the number of Microsoft Teams activities by activity type.
        The activities are performed by Microsoft Teams licensed users.
        """
        return create_report_query(self, "getTeamsUserActivityCounts", period)

    @odata(name="authenticationMethods", navigation=True)
    @property
    def authentication_methods(self) -> AuthenticationMethodsRoot:
        """Container for navigation properties for Azure AD authentication methods resources."""
        return self.properties.get(
            "authenticationMethods",
            AuthenticationMethodsRoot(self.context, ResourcePath("authenticationMethods", self.resource_path)),
        )

    @odata(name="partners", navigation=True)
    @property
    def partners(self) -> Partners:
        """Represents billing details for a Microsoft direct partner."""
        return self.properties.get("partners", Partners(self.context, ResourcePath("partners", self.resource_path)))

    @odata(name="security", navigation=True)
    @property
    def security(self) -> SecurityReportsRoot:
        """Container for navigation properties for Azure AD authentication methods resources."""
        return self.properties.get(
            "security", SecurityReportsRoot(self.context, ResourcePath("security", self.resource_path))
        )

    @odata(name="dailyPrintUsageByPrinter", navigation=True)
    @property
    def daily_print_usage_by_printer(self) -> EntityCollection[PrintUsageByPrinter]:
        """Gets the dailyPrintUsageByPrinter property"""
        return self.properties.get(
            "dailyPrintUsageByPrinter",
            EntityCollection[PrintUsageByPrinter](
                self.context, PrintUsageByPrinter, ResourcePath("dailyPrintUsageByPrinter", self.resource_path)
            ),
        )

    @odata(name="dailyPrintUsageByUser", navigation=True)
    @property
    def daily_print_usage_by_user(self) -> EntityCollection[PrintUsageByUser]:
        """Gets the dailyPrintUsageByUser property"""
        return self.properties.get(
            "dailyPrintUsageByUser",
            EntityCollection[PrintUsageByUser](
                self.context, PrintUsageByUser, ResourcePath("dailyPrintUsageByUser", self.resource_path)
            ),
        )

    @odata(name="monthlyPrintUsageByPrinter", navigation=True)
    @property
    def monthly_print_usage_by_printer(self) -> EntityCollection[PrintUsageByPrinter]:
        """Gets the monthlyPrintUsageByPrinter property"""
        return self.properties.get(
            "monthlyPrintUsageByPrinter",
            EntityCollection[PrintUsageByPrinter](
                self.context, PrintUsageByPrinter, ResourcePath("monthlyPrintUsageByPrinter", self.resource_path)
            ),
        )

    @odata(name="monthlyPrintUsageByUser", navigation=True)
    @property
    def monthly_print_usage_by_user(self) -> EntityCollection[PrintUsageByUser]:
        """Gets the monthlyPrintUsageByUser property"""
        return self.properties.get(
            "monthlyPrintUsageByUser",
            EntityCollection[PrintUsageByUser](
                self.context, PrintUsageByUser, ResourcePath("monthlyPrintUsageByUser", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ReportRoot"

    def get_relying_party_detailed_summary(self, period: str) -> EntityCollection[RelyingPartyDetailedSummary]:
        """getRelyingPartyDetailedSummary operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.relying_party_detailed_summary import RelyingPartyDetailedSummary

        return_type = EntityCollection(self.context, RelyingPartyDetailedSummary)
        qry = FunctionQuery(self, "getRelyingPartyDetailedSummary", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_email_app_usage_versions_user_counts(self, period: str) -> ClientResult[bytes]:
        """getEmailAppUsageVersionsUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(
            self, "getEmailAppUsageVersionsUserCounts", {"period": period}, return_type, return_raw_content=True
        )
        self.context.add_query(qry)
        return return_type

    def get_m365_app_platform_user_counts(self, period: str) -> ClientResult[bytes]:
        """getM365AppPlatformUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(
            self, "getM365AppPlatformUserCounts", {"period": period}, return_type, return_raw_content=True
        )
        self.context.add_query(qry)
        return return_type

    def get_office365_activations_user_detail(self) -> ClientResult[Report]:
        """getOffice365ActivationsUserDetail operation."""
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOffice365ActivationsUserDetail", None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_office365_active_user_counts(self, period: str) -> ClientResult[Report]:
        """getOffice365ActiveUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOffice365ActiveUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_office365_active_user_detail(self, period: str) -> ClientResult[Report]:
        """getOffice365ActiveUserDetail operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOffice365ActiveUserDetail", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_office365_groups_activity_counts(self, period: str) -> ClientResult[Report]:
        """getOffice365GroupsActivityCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOffice365GroupsActivityCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_office365_groups_activity_detail(self, period: str) -> ClientResult[Report]:
        """getOffice365GroupsActivityDetail operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOffice365GroupsActivityDetail", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_office365_groups_activity_file_counts(self, period: str) -> ClientResult[Report]:
        """getOffice365GroupsActivityFileCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOffice365GroupsActivityFileCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_office365_groups_activity_group_counts(self, period: str) -> ClientResult[Report]:
        """getOffice365GroupsActivityGroupCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOffice365GroupsActivityGroupCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_office365_groups_activity_storage(self, period: str) -> ClientResult[Report]:
        """getOffice365GroupsActivityStorage operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOffice365GroupsActivityStorage", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_office365_services_user_counts(self, period: str) -> ClientResult[Report]:
        """getOffice365ServicesUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOffice365ServicesUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_onedrive_usage_account_counts(self, period: str) -> ClientResult[Report]:
        """getOneDriveUsageAccountCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOneDriveUsageAccountCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_onedrive_usage_account_detail(self, period: str) -> ClientResult[Report]:
        """getOneDriveUsageAccountDetail operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getOneDriveUsageAccountDetail", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_sharepoint_activity_file_counts(self, period: str) -> ClientResult[Report]:
        """getSharePointActivityFileCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSharePointActivityFileCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_sharepoint_site_usage_file_counts(self, period: str) -> ClientResult[Report]:
        """getSharePointSiteUsageFileCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSharePointSiteUsageFileCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_sharepoint_site_usage_pages(self, period: str) -> ClientResult[Report]:
        """getSharePointSiteUsagePages operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSharePointSiteUsagePages", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_sharepoint_site_usage_storage(self, period: str) -> ClientResult[Report]:
        """getSharePointSiteUsageStorage operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSharePointSiteUsageStorage", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_activity_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessActivityCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessActivityCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_activity_user_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessActivityUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessActivityUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_activity_user_detail(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessActivityUserDetail operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessActivityUserDetail", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_device_usage_distribution_user_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessDeviceUsageDistributionUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(
            self, "getSkypeForBusinessDeviceUsageDistributionUserCounts", {"period": period}, return_type
        )
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_device_usage_user_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessDeviceUsageUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessDeviceUsageUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_device_usage_user_detail(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessDeviceUsageUserDetail operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessDeviceUsageUserDetail", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_organizer_activity_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessOrganizerActivityCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessOrganizerActivityCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_organizer_activity_minute_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessOrganizerActivityMinuteCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessOrganizerActivityMinuteCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_organizer_activity_user_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessOrganizerActivityUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessOrganizerActivityUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_participant_activity_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessParticipantActivityCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessParticipantActivityCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_participant_activity_minute_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessParticipantActivityMinuteCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessParticipantActivityMinuteCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_participant_activity_user_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessParticipantActivityUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessParticipantActivityUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_peer_to_peer_activity_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessPeerToPeerActivityCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessPeerToPeerActivityCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_peer_to_peer_activity_minute_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessPeerToPeerActivityMinuteCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessPeerToPeerActivityMinuteCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_skype_for_business_peer_to_peer_activity_user_counts(self, period: str) -> ClientResult[Report]:
        """getSkypeForBusinessPeerToPeerActivityUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getSkypeForBusinessPeerToPeerActivityUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_teams_device_usage_distribution_user_counts(self, period: str) -> ClientResult[bytes]:
        """getTeamsDeviceUsageDistributionUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(
            self, "getTeamsDeviceUsageDistributionUserCounts", {"period": period}, return_type, return_raw_content=True
        )
        self.context.add_query(qry)
        return return_type

    def get_teams_device_usage_user_counts(self, period: str) -> ClientResult[bytes]:
        """getTeamsDeviceUsageUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(
            self, "getTeamsDeviceUsageUserCounts", {"period": period}, return_type, return_raw_content=True
        )
        self.context.add_query(qry)
        return return_type

    def get_teams_device_usage_user_detail(self, period: str) -> ClientResult[bytes]:
        """getTeamsDeviceUsageUserDetail operation.

        Args:
            period (str):
                period parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(
            self, "getTeamsDeviceUsageUserDetail", {"period": period}, return_type, return_raw_content=True
        )
        self.context.add_query(qry)
        return return_type

    def get_teams_team_activity_counts(self, period: str) -> ClientResult[bytes]:
        """getTeamsTeamActivityCounts operation.

        Args:
            period (str):
                period parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(self, "getTeamsTeamActivityCounts", {"period": period}, return_type, return_raw_content=True)
        self.context.add_query(qry)
        return return_type

    def get_teams_team_activity_detail(self, period: str) -> ClientResult[bytes]:
        """getTeamsTeamActivityDetail operation.

        Args:
            period (str):
                period parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(self, "getTeamsTeamActivityDetail", {"period": period}, return_type, return_raw_content=True)
        self.context.add_query(qry)
        return return_type

    def get_teams_team_activity_distribution_counts(self, period: str) -> ClientResult[bytes]:
        """getTeamsTeamActivityDistributionCounts operation.

        Args:
            period (str):
                period parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(
            self, "getTeamsTeamActivityDistributionCounts", {"period": period}, return_type, return_raw_content=True
        )
        self.context.add_query(qry)
        return return_type

    def get_teams_user_activity_user_detail(self, period: str) -> ClientResult[bytes]:
        """getTeamsUserActivityUserDetail operation.

        Args:
            period (str):
                period parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(
            self, "getTeamsUserActivityUserDetail", {"period": period}, return_type, return_raw_content=True
        )
        self.context.add_query(qry)
        return return_type

    def get_yammer_activity_counts(self, period: str) -> ClientResult[Report]:
        """getYammerActivityCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getYammerActivityCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_yammer_activity_user_counts(self, period: str) -> ClientResult[Report]:
        """getYammerActivityUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getYammerActivityUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_yammer_activity_user_detail(self, period: str) -> ClientResult[Report]:
        """getYammerActivityUserDetail operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getYammerActivityUserDetail", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_yammer_device_usage_distribution_user_counts(self, period: str) -> ClientResult[Report]:
        """getYammerDeviceUsageDistributionUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getYammerDeviceUsageDistributionUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_yammer_device_usage_user_counts(self, period: str) -> ClientResult[Report]:
        """getYammerDeviceUsageUserCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getYammerDeviceUsageUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_yammer_device_usage_user_detail(self, period: str) -> ClientResult[Report]:
        """getYammerDeviceUsageUserDetail operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getYammerDeviceUsageUserDetail", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_yammer_groups_activity_counts(self, period: str) -> ClientResult[Report]:
        """getYammerGroupsActivityCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getYammerGroupsActivityCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_yammer_groups_activity_detail(self, period: str) -> ClientResult[Report]:
        """getYammerGroupsActivityDetail operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getYammerGroupsActivityDetail", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_yammer_groups_activity_group_counts(self, period: str) -> ClientResult[Report]:
        """getYammerGroupsActivityGroupCounts operation.

        Args:
            period (str):
                period parameter
        """
        from office365.reports.report import Report

        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "getYammerGroupsActivityGroupCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_group_archived_print_jobs(
        self, group_id: str, start_date_time: datetime, end_date_time: datetime
    ) -> ClientResult[ClientValueCollection[ArchivedPrintJob]]:
        """getGroupArchivedPrintJobs operation.

        Args:
            group_id (str):
                groupId parameter
            start_date_time (datetime):
                startDateTime parameter
            end_date_time (datetime):
                endDateTime parameter
        """
        from office365.intune.print.archived_print_job import ArchivedPrintJob

        return_type = ClientResult(self.context, ClientValueCollection(ArchivedPrintJob))
        qry = FunctionQuery(
            self,
            "getGroupArchivedPrintJobs",
            {"groupId": group_id, "startDateTime": start_date_time, "endDateTime": end_date_time},
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def get_printer_archived_print_jobs(
        self, printer_id: str, start_date_time: datetime, end_date_time: datetime
    ) -> ClientResult[ClientValueCollection[ArchivedPrintJob]]:
        """getPrinterArchivedPrintJobs operation.

        Args:
            printer_id (str):
                printerId parameter
            start_date_time (datetime):
                startDateTime parameter
            end_date_time (datetime):
                endDateTime parameter
        """
        from office365.intune.print.archived_print_job import ArchivedPrintJob

        return_type = ClientResult(self.context, ClientValueCollection(ArchivedPrintJob))
        qry = FunctionQuery(
            self,
            "getPrinterArchivedPrintJobs",
            {"printerId": printer_id, "startDateTime": start_date_time, "endDateTime": end_date_time},
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def get_user_archived_print_jobs(
        self, user_id: str, start_date_time: datetime, end_date_time: datetime
    ) -> ClientResult[ClientValueCollection[ArchivedPrintJob]]:
        """getUserArchivedPrintJobs operation.

        Args:
            user_id (str):
                userId parameter
            start_date_time (datetime):
                startDateTime parameter
            end_date_time (datetime):
                endDateTime parameter
        """
        from office365.intune.print.archived_print_job import ArchivedPrintJob

        return_type = ClientResult(self.context, ClientValueCollection(ArchivedPrintJob))
        qry = FunctionQuery(
            self,
            "getUserArchivedPrintJobs",
            {"userId": user_id, "startDateTime": start_date_time, "endDateTime": end_date_time},
            return_type,
        )
        self.context.add_query(qry)
        return return_type
