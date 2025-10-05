from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.refiner.entry import RefinerEntry


class Refiner(ClientValue):

    def __init__(
        self,
        entries: ClientValueCollection[RefinerEntry] = ClientValueCollection(
            RefinerEntry
        ),
        name: str = None,
    ):
        """A refiner contains a list with entries, of the RefinerEntry types"""
        self.Entries = entries
        self.Name = name

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.Refiner"
