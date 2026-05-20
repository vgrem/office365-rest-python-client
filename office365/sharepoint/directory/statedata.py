from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class StateData(ClientValue):
    AdapterName: str | None = None
    Value: bytes | None = None
    ValueJsonString: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.StateData"
