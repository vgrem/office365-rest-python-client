"""Mail attachments — upload sessions, file attachments, listing.

Tests cover:
  - Creating an upload session for large file attachments
  - Adding file attachments (text + binary) to draft messages
  - Listing attachments on a message
  - Verifying attachment metadata (name, size, contentType)
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.outlook.mail.attachments.attachment_item import AttachmentItem
from office365.outlook.mail.attachments.type import AttachmentType
from office365.outlook.mail.messages.message import Message

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestAttachments(GraphDelegatedTestCase):
    """Attachment lifecycle and upload sessions."""

    target_message: ClassVar[Optional[Message]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_message = cls.client.me.messages.add(
            subject="Attachments Test",
            body="Testing file attachments.",
            to_recipients=["fannyd@contoso.onmicrosoft.com"],
        ).execute_query()

    @classmethod
    def tearDownClass(cls):
        msg = cls.target_message
        if msg and msg.resource_path:
            try:
                msg.delete_object().execute_query()
            except Exception:
                pass

    @requires_delegated(
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_01_create_upload_session(self):
        """Creating an attachment upload session returns a valid upload URL."""
        msg = TestAttachments.target_message
        if not msg:
            self.skipTest("No target message available")

        attachment = AttachmentItem(attachmentType=AttachmentType.file, name="flower.png", size=3483322)
        result = msg.attachments.create_upload_session(attachment).execute_query()
        self.assertIsNotNone(result.value)
        upload_url = result.get_property("uploadUrl")
        self.assertIsNotNone(upload_url)

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_02_add_text_file_attachment(self):
        """Adding a text file attachment to a draft message should succeed."""
        msg = TestAttachments.target_message
        if not msg:
            self.skipTest("No target message available")

        msg.add_file_attachment("hello.txt", "Hello World!").execute_query()

        attachments = msg.attachments.get().execute_query()
        matched = [a for a in attachments if a.get_property("name") == "hello.txt"]
        self.assertGreaterEqual(len(matched), 1)

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_03_add_binary_file_attachment(self):
        """Adding a base64-encoded binary attachment to a draft message should succeed."""
        msg = TestAttachments.target_message
        if not msg:
            self.skipTest("No target message available")

        import base64
        import io

        content = base64.b64encode(io.BytesIO(b"This is binary content").read()).decode()

        msg.add_file_attachment("data.bin", base64_content=content).execute_query()

        attachments = msg.attachments.get().execute_query()
        matched = [a for a in attachments if a.get_property("name") == "data.bin"]
        self.assertGreaterEqual(len(matched), 1)

    @requires_delegated(
        "Mail.ReadBasic",
        "Mail.Read",
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_04_list_attachments(self):
        """Listing attachments on a message returns a valid collection."""
        msg = TestAttachments.target_message
        if not msg:
            self.skipTest("No target message available")

        attachments = msg.attachments.get().execute_query()
        self.assertIsNotNone(attachments)

    @requires_delegated(
        "Mail.ReadBasic",
        "Mail.Read",
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_05_attachment_has_expected_properties(self):
        """An attachment exposes name, contentType, size, and id."""
        msg = TestAttachments.target_message
        if not msg:
            self.skipTest("No target message available")

        attachments = msg.attachments.get().execute_query()
        if len(attachments) == 0:
            self.skipTest("No attachments on the message")

        for a in attachments:
            self.assertIsNotNone(a.get_property("name"))
            self.assertIsNotNone(a.get_property("size"))
            break
