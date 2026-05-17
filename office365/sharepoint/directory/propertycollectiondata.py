from office365.runtime.client_value import ClientValue
from typing import Optional


class PropertyCollectionData(ClientValue):
    def __init__(self, total_count: Optional[int] = None):
        self.TotalCount = total_count

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.PropertyCollectionData"
