from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.syntexcustommodeldeploymentproperties import SyntexCustomModelDeploymentProperties


@dataclass
class SyntexCustomModelSetting(ClientValue):
    AnalyzerId: str | None = None
    AzureResourceId: str | None = None
    DeploymentName: str | None = None
    DeploymentProperties: SyntexCustomModelDeploymentProperties = field(
        default_factory=SyntexCustomModelDeploymentProperties
    )
    Endpoint: str | None = None
    EndpointType: int | None = None
    IsDisabled: bool | None = None
    TaskType: int | None = None
    UniqueId: str | None = None
    UniqueName: str | None = None
    Updated: datetime | None = field(default_factory=lambda: datetime.min)
