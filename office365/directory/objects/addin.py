from typing import Dict
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class AddIn(ClientValue):

    def __init__(
        self,
        id_: UUID = None,
        properties: ClientValueCollection[Dict] = ClientValueCollection(dict),
        type_: str = None,
    ):
        self.id = id_
        self.properties = properties
        self.type = type_

    @property
    def entity_type_name(self):
        return "microsoft.graph.AddIn"
