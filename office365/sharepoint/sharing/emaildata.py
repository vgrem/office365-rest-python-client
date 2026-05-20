from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class EmailData(ClientValue):
    body: str | None = None
    subject: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.EmailData"
