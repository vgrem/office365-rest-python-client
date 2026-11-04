from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.viva.syntexcustommodeldeploymentmodelinfo import SyntexCustomModelDeploymentModelInfo


@value
class SyntexCustomModelDeploymentProperties(ClientValue):
    Capabilities: dict | None = field(default_factory=dict)
    Model: SyntexCustomModelDeploymentModelInfo = field(default_factory=SyntexCustomModelDeploymentModelInfo)
