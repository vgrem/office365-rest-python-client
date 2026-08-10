from __future__ import annotations

from office365.directory.permissions.identity import Identity


class EmailIdentity(Identity):
    email: str | None = None
    "Represents the email identity of a user."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EmailIdentity"
