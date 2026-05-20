from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RelationData(ClientValue):
    AttributeDataSource: int | None = None
    TargetObjectId: str | None = None
    TargetObjectSubtype: int | None = None
    TargetObjectType: int | None = None
    Value: bytes | None = None
    ValueJsonString: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.RelationData"
