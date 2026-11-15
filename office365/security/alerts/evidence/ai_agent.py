from __future__ import annotations

from office365.security.ai_agent_platform import AiAgentPlatform
from office365.security.alerts.evidence.base import AlertEvidence


class AiAgentEvidence(AlertEvidence):
    agentId: str | None = None
    agentName: str | None = None
    instructions: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AiAgentEvidence"

    hostingPlatformType: AiAgentPlatform = AiAgentPlatform.unknown
