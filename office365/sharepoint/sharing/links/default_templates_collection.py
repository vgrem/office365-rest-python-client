from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.links.default_template import (
    SharingLinkDefaultTemplate,
)


@dataclass
class SharingLinkDefaultTemplatesCollection(ClientValue):
    templates: ClientValueCollection[SharingLinkDefaultTemplate] = field(
        default_factory=lambda: ClientValueCollection(SharingLinkDefaultTemplate)
    )

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkDefaultTemplatesCollection"
