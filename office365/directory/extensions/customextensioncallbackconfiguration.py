from datetime import timedelta
from typing import Optional

from office365.runtime.client_value import ClientValue


class CustomExtensionCallbackConfiguration(ClientValue):
    def __init__(self, timeout_duration: Optional[timedelta] = None):
        self.timeoutDuration = timeout_duration

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionCallbackConfiguration"
