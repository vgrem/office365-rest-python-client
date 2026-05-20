from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharingAbilityStatus(ClientValue):
    """
    Represents the status for a specific sharing capability for the current user.

    Fields:
        disabledReason: Indicates the reason why the capability is disabled if the capability is disabled
            for any reason.
        enabled: Indicates whether capability is enabled.
    """

    disabledReason: str | None = None
    enabled: bool | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingAbilityStatus"
