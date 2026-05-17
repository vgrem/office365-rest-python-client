from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.syntexcustommodeldeploymentmodelinfo import (
    SyntexCustomModelDeploymentModelInfo,
)


class SyntexCustomModelDeploymentProperties(ClientValue):
    def __init__(
        self,
        capabilities: Optional[dict] = None,
        model: SyntexCustomModelDeploymentModelInfo = SyntexCustomModelDeploymentModelInfo(),
    ):
        self.capabilities = capabilities
        self.model = model
