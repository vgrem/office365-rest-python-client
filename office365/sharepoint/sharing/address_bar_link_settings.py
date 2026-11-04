from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AddressBarLinkSettings(ClientValue):
    linkDisabled: bool | None = None
    linkPermission: int | None = None

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.AddressBarLinkSettings"
