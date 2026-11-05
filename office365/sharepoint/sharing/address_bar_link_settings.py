from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AddressBarLinkSettings(ClientValue):
    linkDisabled: bool | None = None
    linkPermission: int | None = None

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.AddressBarLinkSettings"
