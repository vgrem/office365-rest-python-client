from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SharingLinkExpirationAbilityStatus(ClientValue):
    defaultExpirationInDays: int | None = None
    maxExpirationInDays: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkExpirationAbilityStatus"
