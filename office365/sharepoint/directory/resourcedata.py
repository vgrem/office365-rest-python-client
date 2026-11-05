from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ResourceData(ClientValue):
    ErrorCode: int | None = None
    ErrorMessage: str | None = None
    ResourceAction: int | None = None
    State: int | None = None
    Value: bytes | None = None
    ValueJsonString: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.ResourceData"
