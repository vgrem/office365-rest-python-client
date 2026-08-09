from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class PreAuthorizedApplication(ClientValue):
    appId: str | None = None
    delegatedPermissionIds: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PreAuthorizedApplication"
