from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteTemplate(ClientValue):
    def __init__(self, name: Optional[str] = None):
        self.name = name
