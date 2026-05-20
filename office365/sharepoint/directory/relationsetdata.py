from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RelationSetData(ClientValue):
    TotalCount: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.RelationSetData"
