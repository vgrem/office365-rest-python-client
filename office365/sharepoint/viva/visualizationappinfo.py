from typing import Optional

from office365.runtime.client_value import ClientValue


class VisualizationAppInfo(ClientValue):
    def __init__(self, design_uri: Optional[str] = None, id_: Optional[str] = None, runtime_uri: Optional[str] = None):
        self.design_uri = design_uri
        self.id = id_
        self.runtime_uri = runtime_uri
