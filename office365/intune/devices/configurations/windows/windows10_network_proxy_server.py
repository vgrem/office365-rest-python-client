from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class Windows10NetworkProxyServer(ClientValue):
    address: str | None = None
    exceptions: StringCollection = field(default_factory=StringCollection)
    useForLocalAddresses: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Windows10NetworkProxyServer"
