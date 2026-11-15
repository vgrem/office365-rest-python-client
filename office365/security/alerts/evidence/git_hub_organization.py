from __future__ import annotations

from office365.security.alerts.evidence.base import AlertEvidence


class GitHubOrganizationEvidence(AlertEvidence):
    company: str | None = None
    displayName: str | None = None
    email: str | None = None
    login: str | None = None
    orgId: str | None = None
    webUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.GitHubOrganizationEvidence"
