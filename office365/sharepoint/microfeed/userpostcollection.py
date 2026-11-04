from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.social.microfeed.user_posts import MicrofeedUserPosts


@value
class MicrofeedUserPostCollection(ClientValue):
    Items: ClientValueCollection[MicrofeedUserPosts] = field(
        default_factory=lambda: ClientValueCollection(MicrofeedUserPosts)
    )

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedUserPostCollection"
