from __future__ import annotations

from office365.directory.permissions.identity import Identity


class CommunicationsGuestIdentity(Identity):
    email: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CommunicationsGuestIdentity"
