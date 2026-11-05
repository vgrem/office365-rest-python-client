from __future__ import annotations

from office365.runtime.client_value import ClientValue


class GitHubUserEvidence(ClientValue):
    email: str | None = None
    login: str | None = None
    name: str | None = None
    userId: str | None = None
    webUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.GitHubUserEvidence"
