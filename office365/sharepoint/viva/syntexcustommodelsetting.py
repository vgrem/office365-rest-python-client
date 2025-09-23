from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.syntexcustommodeldeploymentproperties import (
    SyntexCustomModelDeploymentProperties,
)


class SyntexCustomModelSetting(ClientValue):

    def __init__(
        self,
        analyzer_id: str = None,
        azure_resource_id: str = None,
        deployment_name: str = None,
        deployment_properties: SyntexCustomModelDeploymentProperties = SyntexCustomModelDeploymentProperties(),
        endpoint: str = None,
        endpoint_type: int = None,
        is_disabled: bool = None,
        task_type: int = None,
        unique_id: str = None,
        unique_name: str = None,
        updated: datetime = None,
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
