from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class TenantServiceInfoValue(ClientValue):
    deletedDateTime: str | None = None
    objectId: str | None = None
    serviceElements: StringCollection = field(default_factory=StringCollection)
    serviceInstance: str | None = None
    version: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "SP.Directory.TenantServiceInfoValue"
