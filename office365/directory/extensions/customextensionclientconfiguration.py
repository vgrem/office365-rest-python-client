from office365.runtime.client_value import ClientValue


class CustomExtensionClientConfiguration(ClientValue):
    def __init__(self, maximum_retries: int = None, timeout_in_milliseconds: int = None):
        self.maximumRetries = maximum_retries
        self.timeoutInMilliseconds = timeout_in_milliseconds

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionClientConfiguration"
