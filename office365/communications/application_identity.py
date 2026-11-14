from __future__ import annotations

from office365.directory.permissions.identity import Identity


class CommunicationsApplicationIdentity(Identity):
    applicationType: str | None = None
    hidden: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CommunicationsApplicationIdentity"
