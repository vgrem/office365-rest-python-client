import base64
import io
from typing import Optional

from office365.outlook.mail.messages.message import Message
from office365.outlook.mail.recipient import Recipient

from tests import test_user_principal_name, test_user_principal_name_alt
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOutlookMessages(GraphDelegatedTestCase):
    target_message: Optional[Message] = None

    @requires_delegated("Mail.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test2_create_draft_message(self):
        draft_message = self.client.me.messages.add(
            subject="Meet for lunch?", body="The new cafeteria is open."
        ).execute_query()
        self.assertIsNotNone(draft_message.id)
        TestOutlookMessages.target_message = draft_message

    # def test4_create_reply(self):
    #    message = self.__class__.target_message.create_reply().execute_query()
    #    self.assertIsNotNone(message.resource_path)

    # def test4_forward_message(self):
    #    self.__class__.target_message.forward([test_user_principal_name_alt]).execute_query()

    @requires_delegated(
        "Mail.ReadBasic", "Mail.ReadWrite", "Mail.Read", or_roles=["Exchange Administrator", "Global Administrator"]
    )
    def test5_list_my_messages(self):
        """Test listing my messages."""
        result = self.client.me.messages.top(1).get().execute_query()
        self.assertLessEqual(1, len(result))
        self.assertIsNotNone(result[0].resource_path)

    @requires_delegated("Mail.Read", "Mail.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test6_search_messages(self):
        """Test searching messages."""
        result = self.client.me.messages.search("Meet for lunch").execute_query()
        self.assertLessEqual(1, len(result))
        self.assertIsNotNone(result[0].resource_path)

    @requires_delegated("Mail.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test7_update_message(self):
        """Test updating a draft message."""
        assert TestOutlookMessages.target_message is not None
        message = TestOutlookMessages.target_message
        message.body = "The new cafeteria is close."
        message.update().execute_query()

    @requires_delegated("Mail.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test8_delete_message(self):
        """Test deleting a draft message."""
        assert TestOutlookMessages.target_message is not None
        message = TestOutlookMessages.target_message
        message.delete_object().execute_query()

    @requires_delegated("Mail.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test9_create_draft_message_with_attachments(self):
        content = base64.b64encode(io.BytesIO(b"This is some file content").read()).decode()

        draft = (
            self.client.me.messages.add(subject="Check out this attachment", body="The new cafeteria is open.")
            .add_file_attachment("TextAttachment.txt", "Hello World!")
            .add_file_attachment("BinaryAttachment.txt", base64_content=content)
            .execute_query()
        )
        assert draft.id is not None
        expected_count = 2
        attachments = self.client.me.messages[draft.id].attachments.get().execute_query()
        assert len(attachments) == expected_count
        draft.delete_object().execute_query()

    @requires_delegated("Mail.Send", "Mail.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test10_send_message(self):
        message = self.client.me.messages.add(subject="Meet for lunch?", body="The new cafeteria is open.")
        message.to_recipients.add(Recipient.from_email(test_user_principal_name))
        message.to_recipients.add(Recipient.from_email(test_user_principal_name_alt))
        message.body = "The new cafeteria is open."
        message.update().send().execute_query()
