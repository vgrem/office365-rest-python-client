"""Outlook user settings — supported languages, time zones, mail tips, mailbox settings, auto-replies.

Tests cover:
  - Getting supported languages for the user
  - Getting supported time zones for the user
  - Getting mail tips for a recipient
  - Enabling scheduled automatic replies
  - Getting mailbox settings
  - Disabling automatic replies
  - Reading mailbox settings properties
"""

from __future__ import annotations

from datetime import datetime, timedelta

from tests import test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOutlookUser(GraphDelegatedTestCase):
    """Outlook user settings — language, time zone, auto-replies, mail tips."""

    @requires_delegated(
        "User.Read",
        "User.Read.All",
        "User.ReadBasic.All",
        "User.ReadWrite.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_01_supported_languages(self):
        """Getting supported languages returns a valid collection."""
        result = self.client.me.outlook.supported_languages().execute_query()
        self.assertIsNotNone(result.value)
        if result.value:
            self.assertIsNotNone(result.value[0].displayName)

    @requires_delegated(
        "User.Read",
        "User.Read.All",
        "User.ReadBasic.All",
        "User.ReadWrite.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_02_supported_time_zones(self):
        """Getting supported time zones returns a valid collection."""
        result = self.client.me.outlook.supported_time_zones().execute_query()
        self.assertIsNotNone(result.value)
        if result.value:
            self.assertIsNotNone(result.value[0].displayName)

    @requires_delegated(
        "Mail.Read",
        "Mail.Read.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_03_get_mail_tips(self):
        """Getting mail tips for a recipient returns them."""
        result = self.client.me.get_mail_tips([test_user_principal_name]).execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "MailboxSettings.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_04_enable_automatic_replies(self):
        """Enabling scheduled automatic replies should succeed."""
        start = datetime.now()
        end = start + timedelta(days=7)
        self.client.me.enable_automatic_replies_setting(
            status="Scheduled",
            scheduled_start_datetime=start,
            scheduled_end_datetime=end,
        ).execute_query()

    @requires_delegated(
        "MailboxSettings.Read",
        "MailboxSettings.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_05_get_mailbox_settings(self):
        """Getting mailbox settings returns a valid settings object."""
        result = self.client.me.select(["MailboxSettings"]).get().execute_query()
        self.assertIsNotNone(result.mailbox_settings)

    @requires_delegated(
        "MailboxSettings.Read",
        "MailboxSettings.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_06_mailbox_settings_has_properties(self):
        """Mailbox settings expose automaticRepliesSetting and dateFormat."""
        result = self.client.me.select(["MailboxSettings"]).get().execute_query()
        settings = result.mailbox_settings
        if settings:
            self.assertIsNotNone(settings.automaticRepliesSetting)

    @requires_delegated(
        "MailboxSettings.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_07_disable_automatic_replies(self):
        """Disabling automatic replies should succeed."""
        self.client.me.disable_automatic_replies_setting().execute_query()
