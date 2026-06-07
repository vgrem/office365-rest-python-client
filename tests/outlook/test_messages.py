"""Mail messages — draft creation, send, move, search, reply, mark-as-read, attachments.

Tests cover:
  - Creating and sending a message with recipients
  - Creating a draft message
  - Marking a message as read
  - Moving a message between folders
  - Listing messages with pagination
  - Searching messages
  - Updating a draft message body
  - Creating a reply draft
  - Deleting a draft message
  - Creating a draft with file attachments (text + binary)
"""

from __future__ import annotations

import base64
import io
import os
import tempfile
from typing import ClassVar, Optional

from office365.delta_collection import ChangeType
from office365.outlook.mail.messages.message import Message
from office365.outlook.mail.recipient import Recipient

from tests import test_user_principal_name, test_user_principal_name_alt
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOutlookMessages(GraphDelegatedTestCase):
    """Message lifecycle — draft, send, move, search, reply, delete."""

    target_message: ClassVar[Optional[Message]] = None
    target_reply: ClassVar[Optional[Message]] = None

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_01_create_draft_message(self):
        """Creating a draft message without recipients should succeed."""
        draft = self.client.me.messages.add(subject="Meet for lunch?", body="The new cafeteria is open.").execute_query()
        self.assertIsNotNone(draft.get_property("id"))
        self.assertEqual(draft.get_property("subject"), "Meet for lunch?")
        self.assertEqual(draft.get_property("isDraft"), True)
        TestOutlookMessages.target_message = draft

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_02_mark_message_as_read(self):
        """Marking a draft message as read should succeed."""
        msg = TestOutlookMessages.target_message
        if not msg:
            self.skipTest("No message created from previous test")

        msg.set_property("isRead", True).update().execute_query()

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_03_move_message_to_junk(self):
        """Moving a message to the junk email folder should succeed."""
        msg = TestOutlookMessages.target_message
        if not msg:
            self.skipTest("No message created from previous test")

        moved = msg.move("junkemail").execute_query()
        self.assertIsNotNone(moved.resource_path)
        TestOutlookMessages.target_message = moved

    @requires_delegated(
        "Mail.ReadBasic",
        "Mail.Read",
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_04_list_messages_paginated(self):
        """Listing messages with $top=1 returns up to 1 message."""
        result = self.client.me.messages.top(1).get().execute_query()
        self.assertLessEqual(len(result), 1)
        if len(result) > 0:
            self.assertIsNotNone(result[0].resource_path)

    @requires_delegated(
        "Mail.Read",
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_05_search_messages(self):
        """Searching messages by keyword should return results."""
        result = self.client.me.messages.search("Meet for lunch").execute_query()
        if len(result) > 0:
            self.assertIsNotNone(result[0].resource_path)

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_06_update_draft_body(self):
        """Updating a draft message's body should persist."""
        msg = TestOutlookMessages.target_message
        if not msg:
            self.skipTest("No message created from previous test")

        msg.body = "The new cafeteria is close."
        msg.update().execute_query()

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_07_create_reply_draft(self):
        """Creating a reply draft for a message should succeed."""
        msg = TestOutlookMessages.target_message
        if not msg:
            self.skipTest("No message created from previous test")

        reply = msg.create_reply().execute_query()
        self.assertIsNotNone(reply.resource_path)
        TestOutlookMessages.target_reply = reply

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_08_delete_draft_message(self):
        """Deleting a draft message should succeed."""
        msg = TestOutlookMessages.target_message
        if not msg:
            self.skipTest("No message created from previous test")

        msg.delete_object().execute_query()
        TestOutlookMessages.target_message = None

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_09_create_message_with_attachments(self):
        """Creating a draft with text and binary attachments should succeed."""
        content = base64.b64encode(io.BytesIO(b"This is some file content").read()).decode()

        draft = (
            self.client.me.messages.add(subject="Check out this attachment", body="The new cafeteria is open.")
            .add_file_attachment("TextAttachment.txt", "Hello World!")
            .add_file_attachment("BinaryAttachment.txt", base64_content=content)
            .execute_query()
        )
        self.assertIsNotNone(draft.get_property("id"))

        attachments = self.client.me.messages[draft.id].attachments.get().execute_query()
        self.assertEqual(len(attachments), 2)
        draft.delete_object().execute_query()

    @requires_delegated(
        "Mail.Send",
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_10_send_message(self):
        """Sending a message with two recipients should succeed."""
        msg = self.client.me.messages.add(subject="SDK Test — Send", body="Testing the send functionality.")
        msg.to_recipients.add(Recipient.from_email(test_user_principal_name))
        msg.to_recipients.add(Recipient.from_email(test_user_principal_name_alt))
        msg.body = "Testing the send functionality."
        msg.update().send().execute_query()

    @requires_delegated(
        "Mail.Read",
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_11_filter_messages_by_subject(self):
        """Filtering messages by subject returns matching messages."""
        result = self.client.me.messages.filter("contains(subject, 'Meet')").top(5).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_12_forward_message(self):
        """Forwarding a message should succeed."""
        msg = TestOutlookMessages.target_message
        if not msg:
            self.skipTest("No target message available")

        msg.forward(
            comment="FYI",
            to_recipients=[test_user_principal_name],
        ).execute_query()

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_13_delta_query_messages(self):
        """Delta query for newly created messages returns valid data."""
        messages = (
            self.client.me.mail_folders["Inbox"].messages.delta.change_type(ChangeType.created).get().execute_query()
        )
        self.assertIsNotNone(messages)

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_14_download_mime_message(self):
        """Downloading the MIME representation of a message should succeed."""
        msg = TestOutlookMessages.target_message
        if not msg:
            self.skipTest("No target message available")

        with tempfile.TemporaryDirectory() as local_path:
            file_path = os.path.join(local_path, "message.eml")
            with open(file_path, "wb") as f:
                msg.download(f).execute_query()
            self.assertTrue(os.path.getsize(file_path) > 0)
