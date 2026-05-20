from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.syntexcustommodeldeploymentproperties import (
    SyntexCustomModelDeploymentProperties,
)


@dataclass
class SyntexCustomModelSetting(ClientValue):
    analyzer_id: Optional[str] = None
    azure_resource_id: Optional[str] = None
    deployment_name: Optional[str] = None
    deployment_properties: SyntexCustomModelDeploymentProperties = field(
        default_factory=SyntexCustomModelDeploymentProperties
    )
    endpoint: Optional[str] = None
    endpoint_type: Optional[int] = None
    is_disabled: Optional[bool] = None
    task_type: Optional[int] = None
    unique_id: Optional[str] = None
    unique_name: Optional[str] = None
    updated: Optional[datetime] = None
