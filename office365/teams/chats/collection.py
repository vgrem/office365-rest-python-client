from typing import List, Union

from office365.entity_collection import EntityCollection
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.teams.chats.chat import Chat
from office365.teams.chats.type import ChatType


class ChatCollection(EntityCollection[Chat]):
    """Chat's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, Chat, resource_path)

    def add(self, chat_type: Union[str, ChatType], owner_ids: List[str] = None) -> Chat:
        """
        Create a new chat object.

        Note: Only one one-on-one chat can exist between two members. If a one-on-one chat already exists,
        this operation will return the existing chat and not create a new one.

        :param str chat_type: Specifies the type of chat. Possible values are: group and oneOnOne.
        :param List[str] owner_ids: The list of user IDs of the chat members that are owners.
        """
        if isinstance(chat_type, ChatType):
            chat_type = chat_type.value

        return_type = Chat(self.context)
        return_type.set_property("chatType", chat_type)
        if owner_ids:
            from office365.teams.members.aad_user_conversation import (
                AadUserConversationMember,
            )

            for user_id in owner_ids:
                owner = AadUserConversationMember(self.context)
                owner.set_property("userId", user_id)
                owner.roles.add("owner")
                return_type.members.add_child(owner)
        self.add_child(return_type)
        qry = CreateEntityQuery(self, return_type, return_type)
        self.context.add_query(qry)
        return return_type
