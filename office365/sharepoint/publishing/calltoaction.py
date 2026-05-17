from typing import Optional

from office365.runtime.client_value import ClientValue


class CallToAction(ClientValue):
    def __init__(self, is_transpile_ready: Optional[bool] = None, text: Optional[str] = None, url: Optional[str] = None):
        self.IsTranspileReady = is_transpile_ready
        self.Text = text
        self.Url = url

    @property
    def entity_type_name(self):
        return "SP.Publishing.CallToAction"
