from office365.entity_collection import EntityCollection
from office365.outlook.mail.item_body import ItemBody
from office365.teams.chats.messages.message import ChatMessage


class ChatMessageCollection(EntityCollection[ChatMessage]):
    """Chat message's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, ChatMessage, resource_path)

    def add(self, content: str) -> ChatMessage:
        return super().add(body=ItemBody(content=content))
