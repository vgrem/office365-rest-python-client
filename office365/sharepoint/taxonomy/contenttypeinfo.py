from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ContentTypeInfo(ClientValue):
    Description: str | None = None
    Group: str | None = None
    Id: str | None = None
    IsHidden: bool | None = None
    IsSealed: bool | None = None
    Name: str | None = None
    ParentName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "SP.Taxonomy.ContentTypeSync.ContentTypeInfo"
