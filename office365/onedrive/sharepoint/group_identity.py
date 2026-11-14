from __future__ import annotations

from office365.directory.permissions.identity import Identity


class SharePointGroupIdentity(Identity):
    principalId: str | None = None
    title: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointGroupIdentity"
