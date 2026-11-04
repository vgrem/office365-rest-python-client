from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CustomExtensionClientConfiguration(ClientValue):
    maximumRetries: int | None = None
    timeoutInMilliseconds: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionClientConfiguration"
