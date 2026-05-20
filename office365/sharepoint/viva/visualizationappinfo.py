from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class VisualizationAppInfo(ClientValue):
    design_uri: Optional[str] = None
    id: Optional[str] = None
    runtime_uri: Optional[str] = None
