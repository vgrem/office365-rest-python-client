from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from office365.entity_collection import EntityCollection
from office365.teams.members.conversation import ConversationMember

if TYPE_CHECKING:
    from office365.directory.users.user import User


class ConversationMemberCollection(EntityCollection[ConversationMember]):
    """ """

    def __init__(self, context, resource_path=None):
        super().__init__(context, ConversationMember, resource_path)

    def add(
        self,
        user: str | User,
        roles: list[str],
        visible_history_start_datetime: datetime | None = None,
    ):
        """Add a conversationMember.

        Args:
            user (str or office365.directory.users.user.User): The conversation members that should be added.
              Every user who will participate in the chat, including the user who initiates the create request,
              must be specified in this list. Each member must be assigned a role of owner or guest.
              Guest tenant members must be assigned the guest role
            roles (list[str]): The roles for that user.
            visible_history_start_datetime (datetime.datetime):
        """
        from office365.directory.users.user import User

        return_type = super().add(roles=roles)
        if visible_history_start_datetime is not None:
            return_type.set_property("visibleHistoryStartDateTime", visible_history_start_datetime)

        if isinstance(user, User):
            user.ensure_property("id").after_execute(lambda _: return_type.set_property("userId", user.id))
        else:
            return_type.set_property("userId", user)
        return return_type
