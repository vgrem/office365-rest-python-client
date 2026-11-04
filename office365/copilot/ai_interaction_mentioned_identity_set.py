from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.teams.teamwork.conversation_identity import TeamworkConversationIdentity
from office365.teams.teamwork.tags.identity import TeamworkTagIdentity


@value
class AiInteractionMentionedIdentitySet(ClientValue):
    conversation: TeamworkConversationIdentity = field(default_factory=TeamworkConversationIdentity)
    tag: TeamworkTagIdentity = field(default_factory=TeamworkTagIdentity)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AiInteractionMentionedIdentitySet"
