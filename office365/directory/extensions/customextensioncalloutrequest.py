from typing import Optional

from office365.directory.extensions.customextensiondata import CustomExtensionData
from office365.runtime.client_value import ClientValue


class CustomExtensionCalloutRequest(ClientValue):
    def __init__(self, data=CustomExtensionData(), source: Optional[str] = None, type_: Optional[str] = None):
        self.data = data
        self.source = source
        self.type = type_

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionCalloutRequest"
