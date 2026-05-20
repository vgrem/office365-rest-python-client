from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharingLinkTemplate(ClientValue):
    passwordProtected: bool | None = None
    role: int | None = None
    scope: int | None = None
    variant: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkTemplate"
