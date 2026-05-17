from typing import Optional

from office365.runtime.client_value import ClientValue


class PropertyCollectionData(ClientValue):
    def __init__(self, total_count: Optional[int] = None):
        self.TotalCount = total_count

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.PropertyCollectionData"
