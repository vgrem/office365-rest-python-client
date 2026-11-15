from __future__ import annotations

from office365.security.alerts.evidence.base import AlertEvidence


class GitHubUserEvidence(AlertEvidence):
    email: str | None = None
    login: str | None = None
    name: str | None = None
    userId: str | None = None
    webUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.GitHubUserEvidence"
