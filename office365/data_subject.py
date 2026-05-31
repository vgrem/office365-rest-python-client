from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class DataSubject(ClientValue):
    email: str | None = None
    firstName: str | None = None
    lastName: str | None = None
    residency: str | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.DataSubject'