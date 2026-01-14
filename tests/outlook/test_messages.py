import base64
import io

from office365.outlook.mail.messages.message import Message
from office365.outlook.mail.recipient import Recipient
from tests import test_user_principal_name, test_user_principal_name_alt
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestOutlookMessages(GraphTestCase):
    target_message = None  # type: Message

    @requires_delegated_permission("Mail.ReadWrite")
    def test2_create_draft_message(self):
        draft_message = self.client.me.messages.add(
            subject="Meet for lunch?", body="The new cafeteria is open."
        ).execute_query()
        self.assertIsNotNone(draft_message.id)
        self.__class__.target_message = draft_message

    # def test4_create_reply(self):
    #    message = self.__class__.target_message.create_reply().execute_query()
    #    self.assertIsNotNone(message.resource_path)

    # def test4_forward_message(self):
    #    self.__class__.target_message.forward([test_user_principal_name_alt]).execute_query()

    @requires_delegated_permission("Mail.ReadBasic", "Mail.ReadWrite", "Mail.Read")
    def test5_list_my_messages(self):
        result = self.client.me.messages.top(1).get().execute_query()
        self.assertLessEqual(1, len(result))
        self.assertIsNotNone(result[0].resource_path)

    def test6_search_messages(self):
        result = self.client.me.messages.search("Meet for lunch").execute_query()
        self.assertLessEqual(1, len(result))
        self.assertIsNotNone(result[0].resource_path)

    @requires_delegated_permission("Mail.ReadWrite")
    def test6_update_message(self):
        message = self.__class__.target_message
        message.body = "The new cafeteria is close."
        message.update().execute_query()

    @requires_delegated_permission("Mail.ReadWrite")
    def test7_delete_message(self):
        message = self.__class__.target_message
        message.delete_object().execute_query()

    @requires_delegated_permission("Mail.ReadWrite")
    def test8_create_draft_message_with_attachments(self):
        content = base64.b64encode(io.BytesIO(b"This is some file content").read()).decode()

        draft = (
            self.client.me.messages.add(subject="Check out this attachment", body="The new cafeteria is open.")
            .add_file_attachment("TextAttachment.txt", "Hello World!")
            .add_file_attachment("BinaryAttachment.txt", base64_content=content)
            .execute_query()
        )
        assert len(self.client.me.messages[draft.id].attachments.get().execute_query()) == 2
        draft.delete_object().execute_query()

    @requires_delegated_permission("Mail.Send", "Mail.ReadWrite")
    def test9_send_message(self):
        message = self.client.me.messages.add(subject="Meet for lunch?", body="The new cafeteria is open.")
        message.to_recipients.add(Recipient.from_email(test_user_principal_name))
        message.to_recipients.add(Recipient.from_email(test_user_principal_name_alt))
        message.body = "The new cafeteria is open."
        message.update().send().execute_query()
