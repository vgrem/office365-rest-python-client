from office365.runtime.client_value import ClientValue
from typing import Optional


class SiteTemplate(ClientValue):
    def __init__(self, name: Optional[str] = None):
        self.name = name
