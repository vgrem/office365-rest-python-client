from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from typing import Optional

@dataclass
class PublicErrorDetail(ClientValue):
    code: str | None = None
    message: str | None = None
    target: str | None = None
    'Represents the details of publicError or publicInnerError.'

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.PublicErrorDetail'