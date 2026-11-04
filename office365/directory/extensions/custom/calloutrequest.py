from __future__ import annotations

from dataclasses import field

from office365.directory.extensions.custom.data import CustomExtensionData
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CustomExtensionCalloutRequest(ClientValue):
    data: CustomExtensionData = field(default_factory=CustomExtensionData)
    source: str | None = None
    type: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionCalloutRequest"
