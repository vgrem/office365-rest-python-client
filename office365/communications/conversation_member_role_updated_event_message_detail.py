from __future__ import annotations

from dataclasses import field

from office365.directory.identities.set import IdentitySet
from office365.runtime.types.collections import StringCollection
from office365.teams.chats.event_message_detail import EventMessageDetail
from office365.teams.teamwork.user_identity import TeamworkUserIdentity


class ConversationMemberRoleUpdatedEventMessageDetail(EventMessageDetail):
    conversationMemberRoles: StringCollection = field(default_factory=StringCollection)
    conversationMemberUser: TeamworkUserIdentity = field(default_factory=TeamworkUserIdentity)
    initiator: IdentitySet = field(default_factory=IdentitySet)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConversationMemberRoleUpdatedEventMessageDetail"
