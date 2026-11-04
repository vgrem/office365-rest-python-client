from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.microfeed.entity import MicroBlogEntity


@value
class MicroBlogEntityCollection(ClientValue):
    Items: ClientValueCollection[MicroBlogEntity] = field(default_factory=lambda: ClientValueCollection(MicroBlogEntity))

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicroBlogEntityCollection"
