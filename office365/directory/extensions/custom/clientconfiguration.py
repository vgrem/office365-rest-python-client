from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CustomExtensionClientConfiguration(ClientValue):
    maximumRetries: int | None = None
    timeoutInMilliseconds: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionClientConfiguration"
