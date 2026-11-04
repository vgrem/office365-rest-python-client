from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.microfeed.datalink import MicrofeedDataLink


@value
class MicrofeedDataLinkCollection(ClientValue):
    Items: ClientValueCollection[MicrofeedDataLink] = field(
        default_factory=lambda: ClientValueCollection(MicrofeedDataLink)
    )

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedDataLinkCollection"
