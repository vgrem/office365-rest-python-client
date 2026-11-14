from __future__ import annotations

from office365.security.alerts.evidence import AlertEvidence


class CloudLogonRequestEvidence(AlertEvidence):
    requestId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.CloudLogonRequestEvidence"
