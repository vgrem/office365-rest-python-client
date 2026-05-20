from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SyntexCustomModelDeploymentModelInfo(ClientValue):
    format: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
