from __future__ import annotations

from dataclasses import dataclass, field

from office365.copilot.ai_interaction_mentioned_identity_set import AiInteractionMentionedIdentitySet
from office365.runtime.client_value import ClientValue


@dataclass
class AiInteractionMention(ClientValue):
    mentioned: AiInteractionMentionedIdentitySet = field(default_factory=AiInteractionMentionedIdentitySet)
    mentionId: int | None = None
    mentionText: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AiInteractionMention"
