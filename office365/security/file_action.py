from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class FileAction(ClientValue):
    deviceGroupNames: StringCollection = field(default_factory=StringCollection)
    sha1Column: str | None = None
    sha256Column: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FileAction"
