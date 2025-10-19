from datetime import timedelta

from office365.runtime.client_value import ClientValue


class CustomExtensionCallbackConfiguration(ClientValue):

    def __init__(self, timeout_duration: timedelta = None):
        self.timeoutDuration = timeout_duration

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionCallbackConfiguration"
