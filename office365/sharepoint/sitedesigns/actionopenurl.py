from office365.runtime.client_value import ClientValue
from typing import Optional


class ActionOpenUrl(ClientValue):
    def __init__(self, url: Optional[str] = None):
        self.url = url
