from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.userprofiles.hash_tag import HashTag


class HashTagCollection(Entity):
    """The HashTagCollection class specifies a collection of HashTags. For information about the HashTag type,
    see section 3.1.5.55"""

    @property
    def items(self):
        return self.properties.get("Items", ClientValueCollection(HashTag))

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.HashTagCollection"
