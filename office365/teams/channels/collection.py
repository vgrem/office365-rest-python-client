from __future__ import annotations

from typing import Any

from office365.entity_collection import EntityCollection
from office365.runtime.queries.function import FunctionQuery
from office365.teams.channels.channel import Channel
from office365.teams.chats.messages.collection import ChatMessageCollection


class ChannelCollection(EntityCollection[Channel]):
    """Team's channel collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, Channel, resource_path)

    def add(
        self, display_name: str, description: str | None = None, membership_type: str | None = None, **kwargs: Any
    ) -> Channel:
        """Create a new channel in a Microsoft Team, as specified in the request body.

        Args:
            description (str): Optional textual description for the channel.
            display_name (str): Channel name as it will appear to the user in Microsoft Teams.
            membership_type (str): The type of the channel.
        """
        return super().add(displayName=display_name, description=description, membershipType=membership_type, **kwargs)

    def get_all_messages(self) -> ChatMessageCollection:
        """
        Retrieve messages across all channels in a team, including text, audio, and video conversations.

        Chain ``.filter(...)``/``.select(...)``/``.top(...)`` on the returned
        collection to shape the request.
        """
        return_type = ChatMessageCollection(self.context, self.resource_path)
        qry = FunctionQuery(self, "getAllMessages", None, return_type)
        self.context.add_query(qry)
        return return_type
