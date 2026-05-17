from typing import Optional

from office365.runtime.client_value import ClientValue


class CAAESnippetElement(ClientValue):
    def __init__(self, id_: Optional[str] = None, version: Optional[str] = None):
        self.id = id_
        self.version = version
