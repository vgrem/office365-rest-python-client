from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.microfeed.posts.post import MicrofeedPost


@dataclass
class MicrofeedPostCollection(ClientValue):
    Items: ClientValueCollection[MicrofeedPost] = field(default_factory=lambda: ClientValueCollection(MicrofeedPost))

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPostCollection"
