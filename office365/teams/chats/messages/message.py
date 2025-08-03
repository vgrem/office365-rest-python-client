from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.teams.channels.iIdentity import ChannelIdentity
from office365.teams.chats.event_message_detail import EventMessageDetail
from office365.teams.chats.messages.attachment import ChatMessageAttachment


class ChatMessage(Entity):
    """
    Represents an individual chat message within a channel or chat.
    The message can be a root message or part of a thread that is defined by the replyToId property in the message.
    """

    @property
    def attachments(self) -> ClientValueCollection[ChatMessageAttachment]:
        """The collection of replies."""
        return self.properties.get(
            "attachments", ClientValueCollection(ChatMessageAttachment)
        )

    @property
    def body(self) -> ItemBody:
        """
        Plaintext/HTML representation of the content of the chat message. Representation is specified by the
        contentType inside the body. The content is always in HTML if the chat message contains a chatMessageMention.
        """
        return self.properties.get("body", ItemBody())

    @property
    def channel_identity(self) -> ChannelIdentity:
        """
        If the message was sent in a channel, represents identity of the channel.
        """
        return self.properties.get("channelIdentity", ChannelIdentity())

    @property
    def chat_id(self) -> Optional[str]:
        """
        If the message was sent in a chat, represents the identity of the chat.
        """
        return self.properties.get("chatId", None)

    @property
    def created_datetime(self) -> datetime:
        """Timestamp of when the chat message was created."""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def deleted_datetime(self) -> datetime:
        """Read only. Timestamp at which the chat message was deleted, or null if not deleted."""
        return self.properties.get("deletedDateTime", datetime.min)

    @property
    def event_detail(self) -> EventMessageDetail:
        """If present, represents details of an event that happened in a chat, a channel, or a team,
        for example, adding new members. For event messages, the messageType property will be set to systemEventMessage.
        """
        return self.properties.get("eventDetail", EventMessageDetail())

    @property
    def replies(self) -> EntityCollection[ChatMessage]:
        """
        The collection of replies.
        """
        return self.properties.get(
            "replies",
            EntityCollection(
                self.context, ChatMessage, ResourcePath("replies", self.resource_path)
            ),
        )

    @property
    def subject(self) -> Optional[str]:
        """
        The subject of the chat message, in plaintext.
        """
        return self.properties.get("subject", None)

    @property
    def summary(self) -> Optional[str]:
        """
        Summary text of the chat message that could be used for push notifications and summary views or
        fall back views. Only applies to channel chat messages, not chat messages in a chat.
        """
        return self.properties.get("summary", None)

    @property
    def web_url(self) -> Optional[str]:
        """
        Link to the message in Microsoft Teams.
        """
        return self.properties.get("webUrl", None)

    @property
    def importance(self) -> Optional[str]:
        """
        The importance of the chat message. The possible values are: normal, high, urgent.
        """
        return self.properties.get("importance", None)
