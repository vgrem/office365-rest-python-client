from __future__ import annotations

from datetime import timedelta

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CustomExtensionCallbackConfiguration(ClientValue):
    timeoutDuration: timedelta | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionCallbackConfiguration"
