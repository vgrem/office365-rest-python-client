from __future__ import annotations

from office365.security.alerts.evidence.base import AlertEvidence


class OauthApplicationEvidence(AlertEvidence):
    appId: str | None = None
    displayName: str | None = None
    objectId: str | None = None
    publisher: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.OauthApplicationEvidence"
