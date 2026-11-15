from __future__ import annotations

from office365.security.alerts.evidence.base import AlertEvidence


class AzureResourceEvidence(AlertEvidence):
    resourceId: str | None = None
    resourceName: str | None = None
    resourceType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AzureResourceEvidence"
