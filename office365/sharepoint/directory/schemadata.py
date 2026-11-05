from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SchemaData(ClientValue):
    AttributeDataSource: int | None = None
    DelayLoad: bool | None = None
    IsInitialized: bool | None = None
    Name: str | None = None
    Privacy: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.SchemaData"
