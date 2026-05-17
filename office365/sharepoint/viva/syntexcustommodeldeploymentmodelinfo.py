from office365.runtime.client_value import ClientValue
from typing import Optional


class SyntexCustomModelDeploymentModelInfo(ClientValue):
    def __init__(self, format_: Optional[str] = None, name: Optional[str] = None, version: Optional[str] = None):
        self.format = format_
        self.name = name
        self.version = version
