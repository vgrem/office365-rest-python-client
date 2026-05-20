from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.syntexcustommodeldeploymentmodelinfo import (
    SyntexCustomModelDeploymentModelInfo,
)


@dataclass
class SyntexCustomModelDeploymentProperties(ClientValue):
    capabilities: Optional[dict] = None
    model: SyntexCustomModelDeploymentModelInfo = field(default_factory=SyntexCustomModelDeploymentModelInfo)
