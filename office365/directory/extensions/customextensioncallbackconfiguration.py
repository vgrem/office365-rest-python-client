from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from office365.runtime.client_value import ClientValue


@dataclass
class CustomExtensionCallbackConfiguration(ClientValue):
    timeoutDuration: timedelta | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionCallbackConfiguration"
