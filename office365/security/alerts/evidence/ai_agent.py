from __future__ import annotations

from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.securityforai.ai_agent_platform import AiAgentPlatform


class AiAgentEvidence(AlertEvidence):
    agentId: str | None = None
    agentName: str | None = None
    instructions: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AiAgentEvidence"

    hostingPlatformType: AiAgentPlatform = AiAgentPlatform.unknown
