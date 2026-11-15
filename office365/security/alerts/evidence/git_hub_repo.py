from __future__ import annotations

from office365.security.alerts.evidence.base import AlertEvidence


class GitHubRepoEvidence(AlertEvidence):
    baseUrl: str | None = None
    login: str | None = None
    owner: str | None = None
    ownerType: str | None = None
    repoId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.GitHubRepoEvidence"
