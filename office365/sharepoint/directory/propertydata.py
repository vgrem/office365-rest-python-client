from __future__ import annotations

from office365.runtime.client_value import ClientValue


class PropertyData(ClientValue):
    Value: bytes | None = None
    ValueJsonString: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.PropertyData"
