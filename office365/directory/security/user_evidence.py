from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.stream import Stream
from office365.runtime.client_value import ClientValue


@dataclass
class UserEvidence(ClientValue):
    stream: Stream = field(default_factory=Stream)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.UserEvidence"
