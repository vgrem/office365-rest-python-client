from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.directory.linktarget import LinkTarget


class LinkChange(ClientValue):

    def __init__(
        self,
        added: ClientValueCollection[LinkTarget] = ClientValueCollection(LinkTarget),
        name: str = None,
        removed: ClientValueCollection[LinkTarget] = ClientValueCollection(LinkTarget),
    ):
        self.Added = added
        self.Name = name
        self.Removed = removed

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.LinkChange"
