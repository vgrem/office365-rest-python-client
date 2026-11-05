from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class WindowsInformationProtectionResourceCollection(ClientValue):
    displayName: str | None = None
    resources: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionResourceCollection"
