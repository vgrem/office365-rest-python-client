from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Any, List, Optional, Union

from office365.delta_collection import DeltaCollection
from office365.directory.permissions.require_permission import require_permission
from office365.outlook.mail.item_body import ItemBody
from office365.outlook.mail.recipient import Recipient
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.create_entity import CreateEntityQuery

if TYPE_CHECKING:
    from office365.graph_client import GraphClient
    from office365.outlook.mail.messages.message import Message


def _as_text(request: RequestOptions) -> None:
    """Send the base64 MIME body as ``text/plain`` — Graph's MIME import contract."""
    request.set_header("Content-Type", "text/plain")


class MessageCollection(DeltaCollection["Message"]):
    """ """

    def __init__(self, context: GraphClient, resource_path: Optional[ResourcePath] = None):
        from office365.outlook.mail.messages.message import Message

        super().__init__(context, Message, resource_path)

    @require_permission(
        delegated=["Mail.ReadWrite"],
        application=["Mail.ReadWrite"],
        notes="Create a draft message",
    )
    def add(
        self,
        subject: Optional[str] = None,
        body: Optional[Union[str, ItemBody]] = None,
        to_recipients: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Message:
        """Create a draft of a new message, in JSON form.

        A message that is already a document on disk goes through :meth:`add_from_mime`
        instead, which is a different request contract (base64 ``text/plain``).

        Args:
            subject (str): The subject of the message.
            body (str or ItemBody): The body of the message. It can be in HTML or text format
            to_recipients (list[str]):
        """
        if to_recipients is not None:
            kwargs["toRecipients"] = ClientValueCollection(
                Recipient, [Recipient.from_email(email) for email in to_recipients]
            )
        if body is not None:
            kwargs["body"] = body if isinstance(body, ItemBody) else ItemBody(body)
        if subject is not None:
            kwargs["subject"] = subject

        return super().add(**kwargs)

    @require_permission(
        delegated=["Mail.ReadWrite"],
        application=["Mail.ReadWrite"],
        notes="Create a draft from a MIME document",
    )
    def add_from_mime(self, data: bytes) -> Message:
        """Create a draft from an RFC 822 document — a message as a file holds it.

        The bytes are base64-encoded and posted as ``text/plain``, which is the only
        shape Graph's MIME import accepts; the message's headers supply the recipients,
        subject and date, so there is nothing else to spell. Attachments, encodings and
        nested bodies survive because Exchange parses the document itself.

        Exchange adds two facts of its own: the message arrives as a draft
        (``isDraft: true``, which Graph refuses to clear) and ``receivedDateTime`` is the
        import time, the original date surviving in the ``Date`` header (``sentDateTime``).

        Args:
            data (bytes): the message as an ``.eml`` file holds it — not base64.

        Returns:
            The message to be created; it is populated when the queue executes.
        """
        message = self.create_typed_object()
        self.add_child(message)
        query = CreateEntityQuery(self, base64.b64encode(data), message)
        query.before_execute(_as_text)
        self.context.add_query(query)
        return message

    @require_permission(
        delegated=["Mail.Read", "Mail.ReadWrite"],
        application=["Mail.Read", "Mail.ReadWrite"],
        notes="Search messages",
    )
    def search(self, query_text: str) -> MessageCollection:
        """
        search messages based on a value in specific message properties.
        The results of the search are sorted by the date and time that the message was sent.
        A $search request returns up to 1,000 results
        """

        assert self.resource_path is not None
        return_type = MessageCollection(self.context, self.resource_path)
        return_type.query_options.custom["$search"] = query_text
        return_type.get()
        return return_type
