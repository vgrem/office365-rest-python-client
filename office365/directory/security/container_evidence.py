from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ContainerEvidence(ClientValue):
    args: StringCollection = field(default_factory=StringCollection)
    command: StringCollection = field(default_factory=StringCollection)
    containerId: str | None = None
    isPrivileged: bool | None = None
    name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ContainerEvidence"
