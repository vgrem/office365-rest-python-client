"""Tests for SharePoint utility functions including email, permissions, and principal resolution."""

from __future__ import annotations

from office365.runtime.types.collections import StringCollection
from office365.sharepoint.utilities.email_properties import EmailProperties
from office365.sharepoint.utilities.utility import Utility

from tests import test_user_principal_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestUtility(SPTestCase):
    """Test SharePoint utility features."""

    def test_01_get_current_user_email_addresses(self):
        """Get current user email addresses."""
        result = Utility.get_current_user_email_addresses(self.client).execute_query()
        self.assertIsNotNone(result.value)

    def test_02_get_user_permission_levels(self):
        """Get user permission levels."""
        result = Utility.get_user_permission_levels(self.client).execute_query()
        self.assertIsNotNone(result.value)

    def test_03_send_email(self):
        """Send an email via SharePoint utility."""
        email_props = EmailProperties(
            "The new cafeteria is open.", "Meet for lunch?", StringCollection([test_user_principal_name])
        )
        Utility.send_email(self.client, email_props).execute_query()

    def test_04_expand_groups_to_principals(self):
        """Expand groups to individual principals."""
        owner_group = self.client.web.associated_owner_group.get().execute_query()
        result = Utility.expand_groups_to_principals(self.client, [owner_group.login_name or ""], 10).execute_query()
        self.assertIsNotNone(result.value)

    def test_05_create_email_body_for_invitation(self):
        """Create an email body for an invitation."""
        result = Utility.create_email_body_for_invitation(self.client, "SitePages/Home.aspx").execute_query()
        self.assertIsNotNone(result.value)

    # def test6_log_custom_app_error(self):
    #    result = Utility.log_custom_app_error(
    #        self.client, "App error"
    #    ).execute_query()
    #    self.assertIsNotNone(result.value)

    def test_06_resolve_principal_in_current_context(self):
        """Resolve a principal in the current context."""
        result = Utility.resolve_principal_in_current_context(self.client, "Jon Doe").execute_query()
        self.assertIsNotNone(result.value)
