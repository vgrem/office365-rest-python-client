from datetime import date
from typing import Optional, Union

from office365.directory.authentication.methods.root import AuthenticationMethodsRoot
from office365.directory.permissions.require_permission import require_permission
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.partners.partners import Partners
from office365.reports.internal.queries.create_report_query import (
    create_report_query,
    create_report_stream_query,
)
from office365.reports.print_usage_by_printer import PrintUsageByPrinter
from office365.reports.print_usage_by_user import PrintUsageByUser
from office365.reports.report import Report
from office365.reports.security.root import SecurityReportsRoot
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.odata_property import odata


class ReportRoot(Entity):
    """Represents a container for Azure Active Directory (Azure AD) reporting resources."""

    @require_permission(
        delegated=["DeviceManagementConfiguration.Read.All"], application=["DeviceManagementConfiguration.Read.All"]
    )
    def device_configuration_device_activity(self) -> ClientResult[Report]:
        """
        Metadata for the device configuration device activity report
        """
        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "deviceConfigurationDeviceActivity", None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=["DeviceManagementConfiguration.Read.All"], application=["DeviceManagementConfiguration.Read.All"]
    )
    def device_configuration_user_activity(self) -> ClientResult[Report]:
        """
        Metadata for the device configuration user activity report
        """
        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "deviceConfigurationUserActivity", None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=["DeviceManagementManagedDevices.Read.All"], application=["DeviceManagementManagedDevices.Read.All"]
    )
    def managed_device_enrollment_failure_details(self) -> ClientResult[Report]:
        """ """
        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "managedDeviceEnrollmentFailureDetails", None, return_type)
        self.context.add_query(qry)
        return return_type

    def managed_device_enrollment_top_failures(self, period: Optional[str] = None) -> ClientResult[Report]:
        """
        Note: The Microsoft Graph API for Intune requires an active Intune license for the tenant.
        """
        return_type = ClientResult(self.context, Report())
        qry = FunctionQuery(self, "managedDeviceEnrollmentTopFailures", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_email_activity_counts(self, period: str) -> ClientResult[bytes]:
        """Enables you to understand the trends of email activity (like how many were sent, read, and received)
        in your organization.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values for
              {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return_type = ClientResult(self.context, bytes())
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

    def get_email_activity_user_detail(self, period: str) -> ClientResult[bytes]:
        """Get details about email activity users have performed.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_stream_query(self, "getEmailActivityUserDetail", period)

    def get_email_app_usage_apps_user_counts(self, period: str) -> ClientResult[Report]:
        """Get the count of unique users per email app.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getEmailAppUsageAppsUserCounts", period)

    def get_email_app_usage_user_counts(self, period) -> ClientResult[bytes]:
        """Get the count of unique users that connected to Exchange Online using any email app.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_stream_query(self, "getEmailAppUsageUserCounts", period)

    def get_email_app_usage_user_detail(self, period: str) -> ClientResult[bytes]:
        """Get details about which activities users performed on the various email apps.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_stream_query(self, "getEmailAppUsageUserDetail", period)

    def get_mailbox_usage_storage(self, period: str) -> ClientResult[bytes]:
        """Get the amount of storage used in your organization.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_stream_query(self, "getMailboxUsageStorage", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_m365_app_user_counts(self, period: Optional[str] = None) -> ClientResult[bytes]:
        """
        Get a report that provides the trend in the number of active users for each app (Outlook, Word, Excel,
        PowerPoint, OneNote, and Teams) in your organization.
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(self, "getM365AppUserCounts", {"period": period}, return_type)
        self.context.add_query(qry)
        return return_type

    def get_m365_app_user_detail(self, period_or_date: Optional[Union[date, str]] = None) -> ClientResult[bytes]:
        """
        Get a report that provides the details about which apps and platforms users have used.
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(self, "getM365AppUserDetail", {"period": period_or_date}, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_office365_activation_counts(self):
        """Get the count of Microsoft 365 activations on desktops and devices."""
        return create_report_query(self, "getOffice365ActivationCounts")

    def get_office365_activations_user_counts(self) -> ClientResult[Report]:
        """Get the count of Microsoft 365 activations on desktops and devices."""
        return create_report_query(self, "getOffice365ActivationsUserCounts")

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_onedrive_activity_file_counts(self, period: str) -> ClientResult[Report]:
        """Get the number of unique, licensed users that performed file interactions against any OneDrive account.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getOneDriveActivityFileCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_onedrive_activity_user_counts(self, period: str) -> ClientResult[Report]:
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
    def get_onedrive_usage_file_counts(self, period: str) -> ClientResult[Report]:
        """Get the total number of files across all sites and how many are active files. A file is considered active
        if it has been saved, synced, modified, or shared within the specified time period.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getOneDriveUsageFileCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_onedrive_usage_storage(self, period) -> ClientResult[bytes]:
        """Get the trend on the amount of storage you are using in OneDrive for Business.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_stream_query(self, "getOneDriveUsageStorage", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_mailbox_usage_detail(self, period) -> ClientResult[Report]:
        """Get details about mailbox usage.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getMailboxUsageDetail", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_mailbox_usage_mailbox_counts(self, period: str) -> ClientResult[bytes]:
        """Get the total number of user mailboxes in your organization and how many are active each day of the reporting
        period. A mailbox is considered active if the user sent or read any email.

        Args:
            period (str): Specifies the length of time over which the report is aggregated. The supported values
              for {period_value} are: D7, D30, D90, and D180. These values follow the format Dn where n represents
              the number of days over which the report is aggregated. Required.
        """
        return create_report_stream_query(self, "getMailboxUsageMailboxCounts", period)

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
    def get_teams_user_activity_user_counts(self, period: str) -> ClientResult[Report]:
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

    def get_sharepoint_site_usage_detail(self, period: str) -> ClientResult[Report]:
        """Get details about SharePoint site usage.

        Args:
            period (str): Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getSharePointSiteUsageDetail", period)

    def get_sharepoint_site_usage_site_counts(self, period: str) -> ClientResult[Report]:
        """Get the trend of total and active site count during the reporting period.

        Args:
            period (str): Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        return create_report_query(self, "getSharePointSiteUsageSiteCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_teams_team_counts(self, period: str) -> ClientResult[bytes]:
        """Get the number of teams of a particular type in an instance of Microsoft Teams.

        Args:
            period (str): Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the
            format Dn where n represents the number of days over which the report is aggregated. Required.
        """
        return create_report_stream_query(self, "getTeamsTeamCounts", period)

    @require_permission(delegated=["Reports.Read.All"], application=["Reports.Read.All"])
    def get_teams_user_activity_counts(self, period: str) -> ClientResult[bytes]:
        """
        Get the number of Microsoft Teams activities by activity type.
        The activities are performed by Microsoft Teams licensed users.
        """
        return create_report_stream_query(self, "getTeamsUserActivityCounts", period)

    @odata(name="authenticationMethods")
    @property
    def authentication_methods(self) -> AuthenticationMethodsRoot:
        """Container for navigation properties for Azure AD authentication methods resources."""
        return self.properties.get(
            "authenticationMethods",
            AuthenticationMethodsRoot(self.context, ResourcePath("authenticationMethods", self.resource_path)),
        )

    @property
    def partners(self) -> Partners:
        """Represents billing details for a Microsoft direct partner."""
        return self.properties.get("partners", Partners(self.context, ResourcePath("partners", self.resource_path)))

    @property
    def security(self) -> SecurityReportsRoot:
        """Container for navigation properties for Azure AD authentication methods resources."""
        return self.properties.get(
            "security", SecurityReportsRoot(self.context, ResourcePath("security", self.resource_path))
        )

    @property
    def daily_print_usage_by_printer(self) -> EntityCollection[PrintUsageByPrinter]:
        """Gets the dailyPrintUsageByPrinter property"""
        return self.properties.get(
            "dailyPrintUsageByPrinter",
            EntityCollection[PrintUsageByPrinter](
                self.context, PrintUsageByPrinter, ResourcePath("dailyPrintUsageByPrinter", self.resource_path)
            ),
        )

    @property
    def daily_print_usage_by_user(self) -> EntityCollection[PrintUsageByUser]:
        """Gets the dailyPrintUsageByUser property"""
        return self.properties.get(
            "dailyPrintUsageByUser",
            EntityCollection[PrintUsageByUser](
                self.context, PrintUsageByUser, ResourcePath("dailyPrintUsageByUser", self.resource_path)
            ),
        )

    @property
    def monthly_print_usage_by_printer(self) -> EntityCollection[PrintUsageByPrinter]:
        """Gets the monthlyPrintUsageByPrinter property"""
        return self.properties.get(
            "monthlyPrintUsageByPrinter",
            EntityCollection[PrintUsageByPrinter](
                self.context, PrintUsageByPrinter, ResourcePath("monthlyPrintUsageByPrinter", self.resource_path)
            ),
        )

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
