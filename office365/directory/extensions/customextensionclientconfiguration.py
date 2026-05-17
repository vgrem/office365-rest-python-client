from typing import Optional

from office365.runtime.client_value import ClientValue


class CustomExtensionClientConfiguration(ClientValue):
    def __init__(self, maximum_retries: Optional[int] = None, timeout_in_milliseconds: Optional[int] = None):
        self.maximumRetries = maximum_retries
        self.timeoutInMilliseconds = timeout_in_milliseconds

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionClientConfiguration"
