from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class PublicError(ClientValue):
    code: str | None = None
    details: ClientValueCollection[PublicErrorDetail] = field(default_factory=lambda: ClientValueCollection(PublicErrorDetail))
    innerError: PublicInnerError = field(default_factory=PublicInnerError)
    message: str | None = None
    target: str | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.PublicError'