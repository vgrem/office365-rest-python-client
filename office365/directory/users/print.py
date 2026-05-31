
from office365.entity_collection import EntityCollection
from office365.runtime.client_value import ClientValue


class UserPrint(ClientValue):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserPrint"
