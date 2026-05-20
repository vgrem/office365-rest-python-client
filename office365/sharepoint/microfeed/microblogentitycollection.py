from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.microfeed.entity import MicroBlogEntity


@dataclass
class MicroBlogEntityCollection(ClientValue):
    Items: ClientValueCollection[MicroBlogEntity] = field(default_factory=lambda: ClientValueCollection(MicroBlogEntity))

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicroBlogEntityCollection"
