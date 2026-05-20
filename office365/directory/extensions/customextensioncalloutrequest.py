from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.extensions.customextensiondata import CustomExtensionData
from office365.runtime.client_value import ClientValue


@dataclass
class CustomExtensionCalloutRequest(ClientValue):
    data: CustomExtensionData = field(default_factory=CustomExtensionData)
    source: str | None = None
    type: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionCalloutRequest"
