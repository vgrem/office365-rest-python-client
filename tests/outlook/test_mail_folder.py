from typing import Optional

from office365.outlook.mail.folders.folder import MailFolder

from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestGraphMail(GraphDelegatedTestCase):
    target_mail_folder: Optional[MailFolder] = None

    @requires_delegated_permission_or_role("Mail.ReadWrite", roles=["Exchange Administrator", "Global Administrator"])
    def test1_create_mail_folder(self):
        result = self.client.me.mail_folders.add("ClutterAlt", True).execute_query()
        self.assertIsNotNone(result.resource_path)
        TestGraphMail.target_mail_folder = result

    @requires_delegated_permission_or_role(
        "Mail.ReadBasic", "Mail.ReadWrite", "Mail.Read", roles=["Exchange Administrator", "Global Administrator"]
    )
    def test2_list_mail_folder(self):
        result = self.client.me.mail_folders.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreaterEqual(len(result), 1)

    @requires_delegated_permission_or_role("Mail.ReadWrite", roles=["Exchange Administrator", "Global Administrator"])
    def test3_update_mail_folder(self):
        assert TestGraphMail.target_mail_folder is not None
        folder = TestGraphMail.target_mail_folder
        folder.update().execute_query()
        self.assertIsNotNone(folder.resource_path)

    # @requires_delegated_permission("Mail.ReadWrite")
    # def test4_delete_mail_folder(self):
    #    folder = self.__class__.target_mail_folder
    #    folder.delete_object().execute_query()

    @requires_delegated_permission_or_role("Mail.ReadWrite", roles=["Exchange Administrator", "Global Administrator"])
    def test5_permanent_delete_mail_folder(self):
        assert TestGraphMail.target_mail_folder is not None
        folder = TestGraphMail.target_mail_folder
        folder.permanent_delete().execute_query()
