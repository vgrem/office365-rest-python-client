from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.microfeed.posts.options import MicrofeedPostOptions


class MicrofeedPostOptionCollection(Entity):
    @property
    def items(self) -> ClientValueCollection[MicrofeedPostOptions]:
        """Gets the Items property"""
        return self.properties.get("Items", ClientValueCollection(MicrofeedPostOptions))

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPostOptionCollection"
