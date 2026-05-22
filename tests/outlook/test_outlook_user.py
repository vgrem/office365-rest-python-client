from datetime import datetime, timedelta

from tests import test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOutlookUser(GraphDelegatedTestCase):
    @requires_delegated(
        "User.Read",
        "User.Read.All",
        "User.ReadBasic.All",
        "User.ReadWrite.All",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test1_my_supported_languages(self):
        result = self.client.me.outlook.supported_languages().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "User.Read",
        "User.Read.All",
        "User.ReadBasic.All",
        "User.ReadWrite.All",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test2_my_supported_time_zones(self):
        result = self.client.me.outlook.supported_time_zones().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated("Mail.Read", "Mail.Read.Shared", or_roles=["Exchange Administrator", "Global Administrator"])
    def test4_get_mail_tips(self):
        result = self.client.me.get_mail_tips([test_user_principal_name]).execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated("MailboxSettings.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test5_enable_automatic_replies(self):
        start = datetime.now()
        end = start + timedelta(days=7)
        self.client.me.enable_automatic_replies_setting(
            status="Scheduled",
            scheduled_start_datetime=start,
            scheduled_end_datetime=end,
        ).execute_query()

    @requires_delegated(
        "MailboxSettings.Read", "MailboxSettings.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"]
    )
    def test6_get_mailbox_settings(self):
        result = self.client.me.select(["MailboxSettings"]).get().execute_query()
        self.assertIsNotNone(result.mailbox_settings)

    @requires_delegated("MailboxSettings.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test7_disable_automatic_replies(self):
        self.client.me.disable_automatic_replies_setting().execute_query()
