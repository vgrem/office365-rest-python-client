from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ProcessEntityMapping(ClientValue):
    sha1Column: str | None = None
    sha256Column: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ProcessEntityMapping"
