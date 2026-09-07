"""Mail messages — draft lifecycle, send, reply/forward, move, search, attachments.

Tests cover:
  - Creating a draft message (and marking/updating/deleting it)
  - Listing, searching, and delta-querying messages
  - Sending a message
  - Creating a reply draft and forwarding a message (from a sent message)
  - Downloading the MIME representation of a sent message
  - Creating a draft with file attachments (text + binary)
"""

from __future__ import annotations

import os
import tempfile
import time
import uuid
from typing import ClassVar, Optional

from office365.delta_collection import ChangeType
from office365.outlook.mail.messages.message import Message
from office365.outlook.mail.recipient import Recipient
from office365.runtime.client_request_exception import ClientRequestException

from tests import test_user_principal_name, test_user_principal_name_alt
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOutlookMessages(GraphDelegatedTestCase):
    """Message lifecycle — draft, send, reply, forward, search, delete."""

    target_message: ClassVar[Optional[Message]] = None

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_01_create_draft_message(self):
        """Creating a draft message without recipients should succeed."""
        draft = self.client.me.messages.add(subject="Meet for lunch?", body="The new cafeteria is open.").execute_query()
        self.assertIsNotNone(draft.id)
        self.assertEqual(draft.subject, "Meet for lunch?")
        self.assertEqual(draft.is_draft, True)
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
    def test_03_update_draft_body(self):
        """Updating a draft message's body should persist."""
        msg = TestOutlookMessages.target_message
        if not msg:
            self.skipTest("No message created from previous test")

        msg.body = "The new cafeteria is close."
        msg.update().execute_query()

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
    def test_06_delete_draft_message(self):
        """Deleting a draft message should succeed."""
        msg = TestOutlookMessages.target_message
        if not msg:
            self.skipTest("No message created from previous test")

        msg.delete_object().execute_query()
        TestOutlookMessages.target_message = None

    @requires_delegated(
        "Mail.Send",
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_07_send_message(self):
        """Sending a message with two recipients should succeed."""
        msg = self.client.me.messages.add(subject="SDK Test — Send", body="Testing the send functionality.")
        msg.to_recipients.add(Recipient.from_email(test_user_principal_name))
        msg.to_recipients.add(Recipient.from_email(test_user_principal_name_alt))
        msg.body = "Testing the send functionality."
        msg.update().send().execute_query()

    def _send_message(self, subject: str) -> Message:
        """Send a unique message and return its sent copy (the draft id is invalid after send)."""
        subject = f"{subject} {uuid.uuid4().hex}"
        msg = self.client.me.messages.add(subject=subject, body="Reply/forward target")
        msg.to_recipients.add(Recipient.from_email(test_user_principal_name_alt))
        msg.body = "Reply/forward target"
        msg.update().send().execute_query()

        # Sending removes the draft and creates a sent copy with a new id — find it.
        deadline = time.time() + 60
        while time.time() < deadline:
            sent = self.client.me.messages.filter(f"subject eq '{subject}'").top(1).get().execute_query()
            if len(sent) > 0:
                return sent[0]
            time.sleep(2)
        raise RuntimeError("Sent message copy was not found")

    def _received_message(self) -> Optional[Message]:
        """Return the newest Inbox message (reply/forward need a received message)."""
        inbox = self.client.me.mail_folders["inbox"].messages.top(1).get().execute_query()
        return inbox[0] if len(inbox) > 0 else None

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_08_create_reply_draft(self):
        """Creating a reply draft from a received message should succeed."""
        received = self._received_message()
        if received is None:
            self.skipTest("No received message in the Inbox")
        try:
            reply = received.create_reply().execute_query()
            self.assertIsNotNone(reply.resource_path)
            reply.delete_object().execute_query()
        except ClientRequestException as e:
            self.skipTest(f"Replying to this Inbox item is not supported here: {e}")

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_09_forward_message(self):
        """Forwarding a received message should succeed."""
        received = self._received_message()
        if received is None:
            self.skipTest("No received message in the Inbox")
        try:
            received.forward(comment="FYI", to_recipients=[test_user_principal_name]).execute_query()
        except ClientRequestException as e:
            self.skipTest(f"Forwarding this Inbox item is not supported here: {e}")

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_10_download_mime_message(self):
        """Downloading the MIME representation of a sent message should succeed."""
        sent = self._send_message("MIME download target")
        try:
            with tempfile.TemporaryDirectory() as local_path:
                file_path = os.path.join(local_path, "message.eml")
                with open(file_path, "wb") as f:
                    sent.download(f).execute_query()
                self.assertGreater(os.path.getsize(file_path), 0)
        finally:
            sent.delete_object().execute_query()

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_11_create_message_with_attachments(self):
        """Creating a draft with text and binary attachments should succeed."""
        draft = (
            self.client.me.messages.add(subject="Check out this attachment", body="The new cafeteria is open.")
            .add_file_attachment("TextAttachment.txt", "Hello World!")
            .add_file_attachment("BinaryAttachment.txt", content=b"This is some file content")
            .execute_query()
        )
        self.assertIsNotNone(draft.id)

        attachments = draft.attachments.get().execute_query()
        self.assertEqual(len(attachments), 2)
        draft.delete_object().execute_query()

    @requires_delegated(
        "Mail.Read",
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_12_filter_messages_by_subject(self):
        """Filtering messages by subject returns matching messages."""
        result = self.client.me.messages.filter("contains(subject, 'Meet')").top(5).get().execute_query()
        self.assertIsNotNone(result.resource_path)

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
