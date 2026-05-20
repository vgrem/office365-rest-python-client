from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPListItemVersionChange(ClientValue):
    field_title: str | None = None
    new_value: str | None = None
    previous_value: str | None = None
