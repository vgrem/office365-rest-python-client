from __future__ import annotations

from office365.copilot.ai_interaction_entity import AiInteractionEntity


class AiAgentInfo(AiInteractionEntity):
    blueprintId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AiAgentInfo"
