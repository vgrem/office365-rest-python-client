from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.directory.provider.link_change import LinkChange
from office365.sharepoint.directory.provider.property_change import PropertyChange


class DirectoryObjectChanges(ClientValue):
    def __init__(
        self,
        directory_object_sub_type: Optional[int] = None,
        directory_object_type: Optional[int] = None,
        id_: Optional[str] = None,
        link_changes: ClientValueCollection[LinkChange] = ClientValueCollection(LinkChange),
        property_changes: ClientValueCollection[PropertyChange] = ClientValueCollection(PropertyChange),
    ):
        self.DirectoryObjectSubType = directory_object_sub_type
        self.DirectoryObjectType = directory_object_type
        self.Id = id_
        self.LinkChanges = link_changes
        self.PropertyChanges = property_changes

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.DirectoryObjectChanges"
