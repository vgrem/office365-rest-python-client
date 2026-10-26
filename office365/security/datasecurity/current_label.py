from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.security.datasecurity.application_mode import ApplicationMode


@dataclass
class CurrentLabel(ClientValue):
    applicationMode: ApplicationMode = ApplicationMode.manual
    id: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CurrentLabel"
