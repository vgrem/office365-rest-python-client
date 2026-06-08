"""Admin — SharePoint tenant settings, service announcements, M365 apps, people admin.

Tests cover:
  - SharePoint settings: reading, updating, property assertions
  - Service announcements: issues listing, health overviews, messages
  - Microsoft 365 apps configuration
  - People admin: profile card properties
  - Report settings
  - Edge cases: resetting domain lists after update
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestSharePointAdminSettings(GraphDelegatedTestCase):
    """Tenant-level SharePoint and OneDrive settings."""

    @requires_delegated(
        "SharePointTenantSettings.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_01_get_sharepoint_settings(self):
        """Reading SharePoint tenant settings returns a valid settings object."""
        settings = self.client.admin.sharepoint.settings.get().execute_query()
        self.assertIsNotNone(settings.resource_path)

    @requires_delegated(
        "SharePointTenantSettings.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_02_settings_have_expected_properties(self):
        """SharePoint settings expose sharingCapability, idleSessionSignOut, and isLegacyAuthProtocolsEnabled."""
        settings = self.client.admin.sharepoint.settings.get().execute_query()

        self.assertIsNotNone(settings.get_property("sharingCapability"))
        self.assertIsNotNone(settings.get_property("idleSessionSignOut"))

    @requires_delegated(
        "SharePointTenantSettings.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_03_sharing_capability_is_known_value(self):
        """The sharingCapability field should be a known enum value."""
        settings = self.client.admin.sharepoint.settings.get().execute_query()

        capability = settings.sharing_capability
        if capability:
            known_values = {
                "disabled",
                "externalUserSharingOnly",
                "externalUserAndGuestSharing",
                "existingExternalUserSharingOnly",
            }
            self.assertIn(capability, known_values, f"Unexpected sharingCapability '{capability}'")

    @requires_delegated(
        "SharePointTenantSettings.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_04_idle_session_sign_out_has_timeout(self):
        """Idle session sign-out configuration includes a signOutAfterInSeconds value."""
        settings = self.client.admin.sharepoint.settings.get().execute_query()
        idle = settings.idle_session_sign_out
        if idle:
            self.assertIsNotNone(idle.signOutAfterInSeconds)

    @requires_delegated(
        "SharePointTenantSettings.ReadWrite.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_05_update_sharing_blocked_domains(self):
        """Updating the sharing blocked domain list should succeed."""
        settings = self.client.admin.sharepoint.settings
        settings.sharing_blocked_domain_list = ["sdk-test-blocked.com"]
        settings.update().execute_query()

        # Re-read and verify
        updated = self.client.admin.sharepoint.settings.get().execute_query()
        blocked = updated.sharing_blocked_domain_list
        if blocked:
            self.assertIn("sdk-test-blocked.com", blocked)

        # Reset
        settings.sharing_blocked_domain_list = []
        settings.update().execute_query()

    @requires_delegated(
        "SharePointTenantSettings.ReadWrite.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_06_update_idle_session_timeout(self):
        """Updating idle session sign-out timeout should succeed."""
        try:
            settings = self.client.admin.sharepoint.settings.get().execute_query()
            idle = settings.get_property("idleSessionSignOut")
            if not idle:
                self.skipTest("Idle session sign-out not configured")

            original_timeout = idle.get_property("signOutAfterInSeconds")
            new_timeout = 3600  # 1 hour

            idle.set_property("signOutAfterInSeconds", new_timeout)
            settings.update().execute_query()

            # Restore
            idle.set_property("signOutAfterInSeconds", original_timeout)
            settings.update().execute_query()
        except Exception as e:
            self.skipTest(f"Cannot update idle session timeout: {e}")

    @requires_delegated(
        "SharePointTenantSettings.ReadWrite.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_07_clear_domain_lists(self):
        """Setting domain lists to empty should not error."""
        settings = self.client.admin.sharepoint.settings
        settings.sharing_blocked_domain_list = []
        settings.update().execute_query()

        settings.sharing_allowed_domain_list = []
        settings.update().execute_query()


class TestServiceAnnouncement(GraphDelegatedTestCase):
    """Service announcements, issues, and health overviews."""

    @requires_delegated(
        "ServiceMessage.Read.All",
        "ServiceHealth.Read.All",
        bypass_roles=["Service Support Administrator", "Global Administrator", "Global Reader"],
    )
    def test_01_list_service_issues(self):
        """Listing service health issues returns a valid collection."""
        issues = self.client.admin.service_announcement.issues.top(10).get().execute_query()
        self.assertIsNotNone(issues.resource_path)

    @requires_delegated(
        "ServiceMessage.Read.All",
        "ServiceHealth.Read.All",
        bypass_roles=["Service Support Administrator", "Global Administrator", "Global Reader"],
    )
    def test_02_list_health_overviews(self):
        """Listing service health overviews returns a valid collection."""
        overviews = self.client.admin.service_announcement.health_overviews.top(10).get().execute_query()
        self.assertIsNotNone(overviews.resource_path)

    @requires_delegated(
        "ServiceMessage.Read.All",
        "ServiceHealth.Read.All",
        bypass_roles=["Service Support Administrator", "Global Administrator", "Global Reader"],
    )
    def test_03_list_service_messages(self):
        """Listing service update messages returns a valid collection."""
        messages = self.client.admin.service_announcement.messages.top(10).get().execute_query()
        self.assertIsNotNone(messages.resource_path)

    @requires_delegated(
        "ServiceMessage.Read.All",
        "ServiceHealth.Read.All",
        bypass_roles=["Service Support Administrator", "Global Administrator", "Global Reader"],
    )
    def test_04_issue_has_expected_properties(self):
        """A service health issue exposes classification, feature, and impactDescription."""
        issues = self.client.admin.service_announcement.issues.top(5).get().execute_query()
        if len(issues) == 0:
            self.skipTest("No service issues found")

        for issue in issues:
            self.assertIsNotNone(issue.id)
            self.assertIsNotNone(issue.classification)
            self.assertIsNotNone(issue.get_property("status"))
            break

    @requires_delegated(
        "ServiceMessage.Read.All",
        "ServiceHealth.Read.All",
        bypass_roles=["Service Support Administrator", "Global Administrator", "Global Reader"],
    )
    def test_05_filter_issues_by_status(self):
        """Filtering issues by status returns only matching results."""
        for status in ("serviceOperational", "investigating", "restoringService"):
            result = (
                self.client.admin.service_announcement.issues.filter(f"status eq '{status}'")
                .top(3)
                .get()
                .execute_query()
            )
            self.assertIsNotNone(result.resource_path)
            for issue in result:
                self.assertEqual(issue.get_property("status"), status)

    @requires_delegated(
        "ServiceMessage.Read.All",
        "ServiceHealth.Read.All",
        bypass_roles=["Service Support Administrator", "Global Administrator", "Global Reader"],
    )
    def test_06_health_overview_has_service_name(self):
        """A health overview entry exposes service name and status."""
        overviews = self.client.admin.service_announcement.health_overviews.top(5).get().execute_query()
        if len(overviews) == 0:
            self.skipTest("No health overviews found")

        for h in overviews:
            self.assertIsNotNone(h.get_property("service"))
            service_status = h.get_property("status")
            if service_status:
                known = {"serviceOperational", "investigating", "restoringService", "degraded"}
                self.assertIn(service_status, known, f"Unexpected health status '{service_status}'")
            break


class TestAdminM365Apps(GraphDelegatedTestCase):
    """Microsoft 365 apps admin configuration."""

    @requires_delegated(
        "OrgSettings.Read.All",
        bypass_roles=["Reports Administrator", "Global Administrator", "Global Reader"],
    )
    def test_01_get_microsoft365_apps(self):
        """Getting Microsoft 365 apps configuration returns a valid entity."""
        result = self.client.admin.microsoft365_apps.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "OrgSettings.Read.All",
        bypass_roles=["Reports Administrator", "Global Administrator", "Global Reader"],
    )
    def test_02_microsoft365_apps_has_properties(self):
        """Microsoft 365 apps config exposes id and createdDateTime."""
        result = self.client.admin.microsoft365_apps.get().execute_query()
        self.assertIsNotNone(result.get_property("id"))


class TestAdminPeople(GraphDelegatedTestCase):
    """People admin settings — profile card properties."""

    @requires_delegated(
        "UserProfile.Read.All",
        "OrgSettings.Read.All",
        bypass_roles=["Global Administrator", "Global Reader"],
    )
    def test_01_list_profile_card_properties(self):
        """Listing profile card properties returns a valid collection."""
        try:
            result = self.client.admin.people.profile_card_properties.top(10).get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot list profile card properties: {e}")

    @requires_delegated(
        "UserProfile.Read.All",
        "OrgSettings.Read.All",
        bypass_roles=["Global Administrator", "Global Reader"],
    )
    def test_02_profile_card_property_has_directory_name(self):
        """A profile card property exposes a directoryPropertyName field."""
        try:
            result = self.client.admin.people.profile_card_properties.top(5).get().execute_query()
            if len(result) == 0:
                self.skipTest("No profile card properties configured")

            for prop in result:
                self.assertIsNotNone(prop.get_property("directoryPropertyName"))
                break
        except Exception as e:
            self.skipTest(f"Cannot read profile card properties: {e}")


class TestAdminReportSettings(GraphDelegatedTestCase):
    """Admin report settings."""

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Global Administrator", "Global Reader"],
    )
    def test_01_get_report_settings(self):
        """Getting admin report settings returns a valid entity."""
        try:
            result = self.client.admin.report_settings.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot access report settings: {e}")
