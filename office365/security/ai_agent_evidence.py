from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.ai_agent_platform import AiAgentPlatform


@value
class AiAgentEvidence(ClientValue):
    agentId: str | None = None
    agentName: str | None = None
    instructions: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AiAgentEvidence"

    hostingPlatformType: AiAgentPlatform = AiAgentPlatform.unknown
