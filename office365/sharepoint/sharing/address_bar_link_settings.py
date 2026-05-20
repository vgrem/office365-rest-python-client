from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AddressBarLinkSettings(ClientValue):
    linkDisabled: bool | None = None
    linkPermission: int | None = None

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.AddressBarLinkSettings"
