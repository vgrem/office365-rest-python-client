from office365.outlook.mail.folders.folder import MailFolder
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestGraphMail(GraphTestCase):
    target_mail_folder = None  # type: MailFolder

    @requires_delegated_permission("Mail.ReadWrite")
    def test1_create_mail_folder(self):
        result = self.client.me.mail_folders.add("ClutterAlt", True).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.__class__.target_mail_folder = result

    @requires_delegated_permission("Mail.ReadBasic", "Mail.ReadWrite", "Mail.Read")
    def test2_list_mail_folder(self):
        result = self.client.me.mail_folders.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreaterEqual(len(result), 1)

    @requires_delegated_permission("Mail.ReadWrite")
    def test3_update_mail_folder(self):
        folder = self.__class__.target_mail_folder
        folder.update().execute_query()
        self.assertIsNotNone(folder.resource_path)

    # @requires_delegated_permission("Mail.ReadWrite")
    # def test4_delete_mail_folder(self):
    #    folder = self.__class__.target_mail_folder
    #    folder.delete_object().execute_query()

    @requires_delegated_permission("Mail.ReadWrite")
    def test5_permanent_delete_mail_folder(self):
        folder = self.__class__.target_mail_folder
        folder.permanent_delete().execute_query()
