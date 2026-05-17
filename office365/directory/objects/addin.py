from typing import Dict, Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class AddIn(ClientValue):
    def __init__(
        self,
        id_: Optional[UUID] = None,
        properties: ClientValueCollection[Dict] = ClientValueCollection(dict),
        type_: Optional[str] = None,
    ):
        self.id = id_
        self.properties = properties
        self.type = type_

    @property
    def entity_type_name(self):
        return "microsoft.graph.AddIn"
