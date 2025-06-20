from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Union

from office365.delta_collection import DeltaCollection
from office365.outlook.mail.item_body import ItemBody
from office365.outlook.mail.recipient import Recipient
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath

if TYPE_CHECKING:
    from office365.graph_client import GraphClient
    from office365.outlook.mail.messages.message import Message


class MessageCollection(DeltaCollection["Message"]):
    """ """

    def __init__(self, context: GraphClient, resource_path: ResourcePath = None):
        from office365.outlook.mail.messages.message import Message

        super(MessageCollection, self).__init__(context, Message, resource_path)

    def add(
        self,
        subject: str = None,
        body: Union[str, ItemBody] = None,
        to_recipients: List[str] = None,
        **kwargs: Any,
    ) -> Message:
        """
        Create a draft of a new message in either JSON or MIME format.

        :param str subject: The subject of the message.
        :param str or ItemBody body: The body of the message. It can be in HTML or text format
        :param list[str] to_recipients:
        """
        if to_recipients is not None:
            kwargs["toRecipients"] = ClientValueCollection(
                Recipient, [Recipient.from_email(email) for email in to_recipients]
            )
        if body is not None:
            kwargs["body"] = body if isinstance(body, ItemBody) else ItemBody(body)
        if subject is not None:
            kwargs["subject"] = subject

        return super(MessageCollection, self).add(**kwargs)

    def search(self, query_text: str) -> MessageCollection:
        """
        search messages based on a value in specific message properties.
        The results of the search are sorted by the date and time that the message was sent.
        A $search request returns up to 1,000 results
        """

        return_type = MessageCollection(self.context, self.resource_path)
        return_type.query_options.custom["search"] = query_text
        return_type.get()
        return return_type
