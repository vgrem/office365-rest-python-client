from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.syntexcustommodeldeploymentproperties import (
    SyntexCustomModelDeploymentProperties,
)


class SyntexCustomModelSetting(ClientValue):
    def __init__(
        self,
        analyzer_id: Optional[str] = None,
        azure_resource_id: Optional[str] = None,
        deployment_name: Optional[str] = None,
        deployment_properties: SyntexCustomModelDeploymentProperties = SyntexCustomModelDeploymentProperties(),
        endpoint: Optional[str] = None,
        endpoint_type: Optional[int] = None,
        is_disabled: Optional[bool] = None,
        task_type: Optional[int] = None,
        unique_id: Optional[str] = None,
        unique_name: Optional[str] = None,
        updated: Optional[datetime] = None,
    ):
        self.analyzer_id = analyzer_id
        self.azure_resource_id = azure_resource_id
        self.deployment_name = deployment_name
        self.deployment_properties = deployment_properties
        self.endpoint = endpoint
        self.endpoint_type = endpoint_type
        self.is_disabled = is_disabled
        self.task_type = task_type
        self.unique_id = unique_id
        self.unique_name = unique_name
        self.updated = updated
