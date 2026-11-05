from __future__ import annotations

from office365.runtime.client_value import ClientValue


class PropertyCollectionData(ClientValue):
    TotalCount: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.PropertyCollectionData"
