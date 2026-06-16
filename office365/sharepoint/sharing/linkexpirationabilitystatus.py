from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharingLinkExpirationAbilityStatus(ClientValue):
    defaultExpirationInDays: int | None = None
    maxExpirationInDays: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkExpirationAbilityStatus"
