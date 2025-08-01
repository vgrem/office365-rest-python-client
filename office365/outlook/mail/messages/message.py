from __future__ import annotations

import os
import uuid
from datetime import datetime
from typing import IO, Any, AnyStr, Callable, List, Optional, Tuple, Union

from typing_extensions import Self

from office365.directory.extensions.extended_property import (
    MultiValueLegacyExtendedProperty,
    SingleValueLegacyExtendedProperty,
)
from office365.directory.extensions.extension import Extension
from office365.entity_collection import EntityCollection
from office365.outlook.item import OutlookItem
from office365.outlook.mail.attachments.collection import AttachmentCollection
from office365.outlook.mail.folders.folder import MailFolder
from office365.outlook.mail.item_body import ItemBody
from office365.outlook.mail.messages.followup_flag import FollowupFlag
from office365.outlook.mail.messages.internet_header import InternetMessageHeader
from office365.outlook.mail.recipient import Recipient
from office365.runtime.client_object_meta import persist_property
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery


class Message(OutlookItem):
    """A message in a mailbox folder."""

    def add_extended_property(self, name: str, value: str) -> Self:
        """Create a single-value extended property for a message"""
        prop_id = str(uuid.uuid4())
        prop_type = "String"
        prop_value = [
            {
                "id": f"{prop_type} {{{prop_id}}} Name {name}",
                "value": value,
            }
        ]
        self.set_property("singleValueExtendedProperties", prop_value)
        return self

    def create_forward(
        self,
        to_recipients: List[Recipient] = None,
        message: Message = None,
        comment: str = None,
    ) -> Message:
        """
        Create a draft to forward an existing message, in either JSON or MIME format.

        :param list[Recipient] to_recipients:
        :param Message message:
        :param str comment:
        """
        return_type = Message(self.context)
        payload = {
            "ToRecipients": ClientValueCollection(Recipient, to_recipients),
            "Message": message,
            "Comment": comment,
        }
        qry = ServiceOperationQuery(
            self, "createForward", None, payload, None, return_type
        )
        self.context.add_query(qry)
        return self

    def download(self, file_object: IO) -> Self:
        """Download MIME content of a message into a file"""

        def _save_content(return_type: ClientResult[AnyStr]) -> None:
            file_object.write(return_type.value)

        self.get_content().after_execute(_save_content)
        return self

    def get_content(self) -> ClientResult[bytes]:
        """Get MIME content of a message"""
        return_type = ClientResult(self.context)
        qry = FunctionQuery(self, "$value", None, return_type)
        self.context.add_query(qry)
        return return_type

    def add_file_attachment(
        self, name: str, content=None, content_type=None, base64_content=None
    ):
        """
        Attach a file to message

        :param str name: The name representing the text that is displayed below the icon representing the
             embedded attachment
        :param str or None content: The contents of the file
        :param str or None content_type: The content type of the attachment.
        :param str or None base64_content: The contents of the file in the form of a base64 string.
        """
        if not content and not base64_content:
            raise TypeError("Either content or base64_content is required")
        self.attachments.add_file(name, content, content_type, base64_content)
        return self

    def upload_attachment(
        self, file_path: str, chunk_uploaded: Optional[Callable[[int], None]] = None
    ):
        """
        This approach is used to attach a file if the file size is between 3 MB and 150 MB, otherwise
        if a file that's smaller than 3 MB, then add_file_attachment method is utilized

        :param str file_path:
        :param (int)->None chunk_uploaded: Upload action
        """
        max_upload_chunk = 1000000 * 3
        file_size = os.stat(file_path).st_size
        if file_size > max_upload_chunk:

            def _message_loaded():
                self.attachments.resumable_upload(
                    file_path, max_upload_chunk, chunk_uploaded
                )

            self.ensure_property("id", _message_loaded)
        else:
            with open(file_path, "rb") as file_object:
                content = file_object.read()
            self.attachments.add_file(
                os.path.basename(file_object.name), content.decode("utf-8")
            )
        return self

    def send(self) -> Self:
        """
        Send a message in the draft folder. The draft message can be a new message draft, reply draft, reply-all draft,
        or a forward draft. The message is then saved in the Sent Items folder.
        """
        qry = ServiceOperationQuery(self, "send")
        self.context.add_query(qry)
        return self

    def reply(self, comment: str = None) -> Message:
        """Reply to the sender of a message by specifying a comment and using the Reply method. The message is then
        saved in the Sent Items folder.

        :param str comment: A comment to include. Can be an empty string.
        """
        message = Message(self.context)
        payload = {"message": message, "comment": comment}
        qry = ServiceOperationQuery(self, "reply", None, payload)
        self.context.add_query(qry)
        return message

    def reply_all(self) -> Self:
        """Reply to all recipients of a message. The message is then saved in the Sent Items folder."""
        qry = ServiceOperationQuery(self, "replyAll")
        self.context.add_query(qry)
        return self

    def create_reply(self, comment=None) -> Message:
        """
        Create a draft to reply to the sender of a message in either JSON or MIME format.

        :param str comment:
        """
        return_type = Message(self.context)
        payload = {"comment": comment}
        qry = ServiceOperationQuery(
            self, "createReply", None, payload, None, return_type
        )
        self.context.add_query(qry)
        return self

    def create_reply_all(self) -> Self:
        """
        Create a draft to reply to the sender and all the recipients of the specified message.
        You can then update the draft to add reply content to the body or change other message properties, or,
        simply send the draft.
        """
        qry = ServiceOperationQuery(self, "createReplyAll")
        self.context.add_query(qry)
        return self

    def copy(self, destination: Union[str, MailFolder]) -> Self:
        """
        Copy a message to another folder within the specified user's mailbox.
        This creates a new copy of the message in the destination folder.

        :param str or MailFolder destination: The destination folder ID, or a well-known folder name.
            For a list of supported well-known folder names, see mailFolder resource type.
        """
        from office365.outlook.mail.folders.folder import MailFolder

        def _copy(destination_id: str) -> None:
            payload = {"DestinationId": destination_id}
            qry = ServiceOperationQuery(self, "copy", None, payload, None, None)
            self.context.add_query(qry)

        if isinstance(destination, MailFolder):

            def _loaded():
                _copy(destination.id)

            destination.ensure_property("id", _loaded)
        else:
            _copy(destination)
        return self

    def move(self, destination: Union[str, MailFolder]) -> Self:
        """
        Move a message to another folder within the specified user's mailbox.
        This creates a new copy of the message in the destination folder and removes the original message.

        :param str or MailFolder destination: The destination folder ID, or a well-known folder name.
            For a list of supported well-known folder names, see mailFolder resource type.
        """
        from office365.outlook.mail.folders.folder import MailFolder

        def _move(destination_id: str) -> None:
            payload = {"DestinationId": destination_id}
            qry = ServiceOperationQuery(self, "move", None, payload, None, None)
            self.context.add_query(qry)

        if isinstance(destination, MailFolder):

            def _loaded():
                _move(destination.id)

            destination.ensure_property("id", _loaded)
        else:
            _move(destination)
        return self

    def forward(self, to_recipients: List[str], comment: str = "") -> Self:
        """
        Forward a message. The message is saved in the Sent Items folder.
        :param list[str] to_recipients: The list of recipients.
        :param str comment: A comment to include. Can be an empty string.
        """
        payload = {
            "toRecipients": ClientValueCollection(
                Recipient, [Recipient.from_email(v) for v in to_recipients]
            ),
            "comment": comment,
        }
        qry = ServiceOperationQuery(self, "forward", None, payload)
        self.context.add_query(qry)
        return self

    @property
    def has_attachments(self) -> Optional[bool]:
        """
        Indicates whether the message has attachments. This property doesn't include inline attachments,
        so if a message contains only inline attachments, this property is false. To verify the existence
        of inline attachments, parse the body property to look for a src attribute,
        such as <IMG src="cid:image001.jpg@01D26CD8.6C05F070">.
        """
        return self.properties.get("hasAttachments", None)

    @property
    @persist_property()
    def attachments(self) -> AttachmentCollection:
        """The fileAttachment and itemAttachment attachments for the message."""
        return self.properties.setdefault(
            "attachments",
            AttachmentCollection(
                self.context, ResourcePath("attachments", self.resource_path)
            ),
        )

    @property
    def extensions(self) -> EntityCollection[Extension]:
        """The collection of open extensions defined for the message. Nullable."""
        return self.properties.get(
            "extensions",
            EntityCollection(
                self.context, Extension, ResourcePath("extensions", self.resource_path)
            ),
        )

    @property
    def body(self) -> ItemBody:
        """The body of the message. It can be in HTML or text format."""
        return self.properties.setdefault("body", ItemBody())

    @body.setter
    def body(self, value: Union[str, ItemBody, Tuple]) -> None:
        """Sets the body of the message. It can be in HTML or text format."""
        content_type = "Text"  # Default content type
        if isinstance(value, tuple):
            if len(value) != 2:
                raise ValueError("value must be a tuple of (content, content_type)")
            content, content_type = value
        else:
            content = value
        if isinstance(content, ItemBody):
            self.set_property("body", content)
            return
        if content_type.lower() not in ["text", "html"]:
            raise ValueError("content_type must be either 'Text' or 'HTML'")
        item_body = ItemBody(content=content, content_type=content_type)
        self.set_property("body", item_body)

    @property
    def body_preview(self) -> Optional[str]:
        """The first 255 characters of the message body. It is in text format."""
        return self.properties.get("bodyPreview", None)

    @property
    def conversation_id(self) -> Optional[str]:
        """The ID of the conversation the email belongs to."""
        return self.properties.get("conversationId", None)

    @property
    def conversation_index(self) -> Optional[str]:
        """Indicates the position of the message within the conversation."""
        return self.properties.get("conversationIndex", None)

    @property
    def flag(self) -> FollowupFlag:
        """
        The flag value that indicates the status, start date, due date, or completion date for the message.
        """
        return self.properties.get("flag", FollowupFlag())

    @property
    def sent_from(self) -> Recipient:
        """
        The owner of the mailbox from which the message is sent. In most cases, this value is the same as the sender
        property, except for sharing or delegation scenarios. The value must correspond to the actual mailbox used.
        Find out more about setting the from and sender properties of a message.
        """
        return self.properties.get("from", Recipient())

    @property
    def importance(self) -> Optional[str]:
        """The importance of the message."""
        return self.properties.get("importance", None)

    @property
    def inference_classification(self) -> Optional[str]:
        """
        The classification of the message for the user, based on inferred relevance or importance,
        or on an explicit override. The possible values are: focused or other.
        """
        return self.properties.get("inferenceClassification", None)

    @property
    def internet_message_headers(self) -> ClientValueCollection[InternetMessageHeader]:
        """
        A collection of message headers defined by RFC5322. The set includes message headers indicating the network
        path taken by a message from the sender to the recipient. It can also contain custom message headers that
        hold app data for the message.
        """
        return self.properties.get(
            "internetMessageHeaders", ClientValueCollection(InternetMessageHeader)
        )

    @property
    def internet_message_id(self) -> Optional[str]:
        """The message ID in the format specified by RFC2822"""
        return self.properties.get("internetMessageId", None)

    @property
    def is_delivery_receipt_requested(self) -> Optional[bool]:
        """
        Indicates whether a read receipt is requested for the message.
        """
        return self.properties.get("isDeliveryReceiptRequested", None)

    @property
    def is_draft(self) -> Optional[bool]:
        """
        Indicates whether the message is a draft. A message is a draft if it hasn't been sent yet.
        """
        return self.properties.get("isDraft", None)

    @property
    def is_read(self) -> Optional[bool]:
        """Indicates whether the message has been read."""
        return self.properties.get("isRead", None)

    @property
    def is_read_receipt_requested(self) -> Optional[bool]:
        """
        Indicates whether a read receipt is requested for the message.
        """
        return self.properties.get("isReadReceiptRequested", None)

    @property
    def received_datetime(self) -> datetime:
        """The date and time the message was received."""
        return self.properties.get("receivedDateTime", datetime.min)

    @property
    def sent_datetime(self) -> datetime:
        """The date and time the message was sent."""
        return self.properties.get("sentDateTime", datetime.min)

    @property
    def subject(self) -> Optional[str]:
        """The subject of the message."""
        return self.properties.get("subject", None)

    @subject.setter
    def subject(self, value: str) -> None:
        """Sets the subject of the message."""
        self.set_property("subject", value)

    @property
    @persist_property("toRecipients")
    def to_recipients(self) -> ClientValueCollection[Recipient]:
        """The To: recipients for the message."""
        return self.properties.setdefault(
            "toRecipients", ClientValueCollection(Recipient)
        )

    @property
    @persist_property("bccRecipients")
    def bcc_recipients(self) -> ClientValueCollection[Recipient]:
        """The BCC: recipients for the message."""
        return self.properties.setdefault(
            "bccRecipients", ClientValueCollection(Recipient)
        )

    @property
    @persist_property("ccRecipients")
    def cc_recipients(self) -> ClientValueCollection[Recipient]:
        """The CC: recipients for the message."""
        return self.properties.setdefault(
            "ccRecipients", ClientValueCollection(Recipient)
        )

    @property
    @persist_property("replyTo")
    def reply_to(self) -> ClientValueCollection[Recipient]:
        """The replyTo: recipients for the reply to the message."""
        return self.properties.setdefault("replyTo", ClientValueCollection(Recipient))

    @property
    def sender(self) -> Recipient:
        """The account that is actually used to generate the message. In most cases, this value is the same as the
        from property. You can set this property to a different value when sending a message from a shared mailbox,
        for a shared calendar, or as a delegate. In any case, the value must correspond to the actual mailbox used.
        Find out more about setting the from and sender properties of a message."""
        return self.properties.get("sender", Recipient())

    @property
    def parent_folder_id(self) -> Optional[str]:
        """The unique identifier for the message's parent mailFolder."""
        return self.properties.get("parentFolderId", None)

    @property
    def web_link(self) -> Optional[str]:
        """
        The URL to open the message in Outlook on the web.

        You can append an ispopout argument to the end of the URL to change how the message is displayed.
        If ispopout is not present or if it is set to 1, then the message is shown in a popout window.
        If ispopout is set to 0, then the browser will show the message in the Outlook on the web review pane.

        The message will open in the browser if you are logged in to your mailbox via Outlook on the web.
        You will be prompted to login if you are not already logged in with the browser.

        This URL cannot be accessed from within an iFrame.
        """
        return self.properties.get("webLink", None)

    @property
    def multi_value_extended_properties(
        self,
    ) -> EntityCollection[MultiValueLegacyExtendedProperty]:
        """The collection of multi-value extended properties defined for the event."""
        return self.properties.get(
            "multiValueExtendedProperties",
            EntityCollection(
                self.context,
                MultiValueLegacyExtendedProperty,
                ResourcePath("multiValueExtendedProperties", self.resource_path),
            ),
        )

    @property
    def single_value_extended_properties(
        self,
    ) -> EntityCollection[SingleValueLegacyExtendedProperty]:
        """The collection of single-value extended properties defined for the message"""
        return self.properties.get(
            "singleValueExtendedProperties",
            EntityCollection(
                self.context,
                SingleValueLegacyExtendedProperty,
                ResourcePath("singleValueExtendedProperties", self.resource_path),
            ),
        )

    def get_property(self, name: str, default_value: Any = None) -> Self:
        if default_value is None:
            property_type_mapping = {
                "toRecipients": self.to_recipients,
                "bccRecipients": self.bcc_recipients,
                "ccRecipients": self.cc_recipients,
                "from": self.sent_from,
                "internetMessageHeaders": self.internet_message_headers,
                "multiValueExtendedProperties": self.multi_value_extended_properties,
                "receivedDateTime": self.received_datetime,
                "sentDateTime": self.sent_datetime,
                "singleValueExtendedProperties": self.single_value_extended_properties,
            }
            default_value = property_type_mapping.get(name, None)

        return super(Message, self).get_property(name, default_value)
