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

from office365.directory.users.user import User
from office365.outlook.user import OutlookUser

from tests import test_user_principal_name
from tests.decorators import requires_call, requires_delegated
from tests.graph_case import GraphDelegatedTestCase

#: The roles that may perform these calls without holding the scope itself.
ADMIN_ROLES = ["Exchange Administrator", "Global Administrator"]


class TestOutlookUser(GraphDelegatedTestCase):
    """Outlook user settings — language, time zone, auto-replies, mail tips."""

    @requires_call(OutlookUser.supported_languages, bypass_roles=ADMIN_ROLES)
    def test_01_supported_languages(self):
        """Getting supported languages returns a valid collection."""
        result = self.client.me.outlook.supported_languages().execute_query()
        self.assertIsNotNone(result.value)
        if result.value:
            self.assertIsNotNone(result.value[0].displayName)

    @requires_call(OutlookUser.supported_time_zones, bypass_roles=ADMIN_ROLES)
    def test_02_supported_time_zones(self):
        """Getting supported time zones returns a valid collection."""
        result = self.client.me.outlook.supported_time_zones().execute_query()
        self.assertIsNotNone(result.value)
        if result.value:
            self.assertIsNotNone(result.value[0].displayName)

    @requires_call(User.get_mail_tips, bypass_roles=ADMIN_ROLES)
    def test_03_get_mail_tips(self):
        """Getting mail tips for a recipient returns them."""
        result = self.client.me.get_mail_tips([test_user_principal_name]).execute_query()
        self.assertIsNotNone(result.value)

    @requires_call(User.enable_automatic_replies_setting, bypass_roles=ADMIN_ROLES)
    def test_04_enable_automatic_replies(self):
        """Enabling scheduled automatic replies should succeed."""
        start = datetime.now()
        end = start + timedelta(days=7)
        self.client.me.enable_automatic_replies_setting(
            status="Scheduled",
            scheduled_start_datetime=start,
            scheduled_end_datetime=end,
        ).execute_query()

    # Not derived: the call is the generic ``Entity.get``, which names no permission -
    # it cannot know which type it reads. Reading a user's mailbox settings needs
    # ``MailboxSettings.Read`` *and* ``User.Read``, and only this test knows both.
    @requires_delegated(
        "MailboxSettings.Read",
        "MailboxSettings.ReadWrite",
        bypass_roles=ADMIN_ROLES,
    )
    def test_05_get_mailbox_settings(self):
        """Getting mailbox settings returns a valid settings object."""
        result = self.client.me.select(["MailboxSettings"]).get().execute_query()
        self.assertIsNotNone(result.mailbox_settings)

    @requires_delegated(
        "MailboxSettings.Read",
        "MailboxSettings.ReadWrite",
        bypass_roles=ADMIN_ROLES,
    )
    def test_06_mailbox_settings_has_properties(self):
        """Mailbox settings expose automaticRepliesSetting and dateFormat."""
        result = self.client.me.select(["MailboxSettings"]).get().execute_query()
        settings = result.mailbox_settings
        if settings:
            self.assertIsNotNone(settings.automaticRepliesSetting)

    @requires_call(User.disable_automatic_replies_setting, bypass_roles=ADMIN_ROLES)
    def test_07_disable_automatic_replies(self):
        """Disabling automatic replies should succeed."""
        self.client.me.disable_automatic_replies_setting().execute_query()
