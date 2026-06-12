from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.syntexcustommodeldeploymentmodelinfo import SyntexCustomModelDeploymentModelInfo


@dataclass
class SyntexCustomModelDeploymentProperties(ClientValue):
    Capabilities: dict | None = field(default_factory=dict)
    Model: SyntexCustomModelDeploymentModelInfo = field(default_factory=SyntexCustomModelDeploymentModelInfo)
