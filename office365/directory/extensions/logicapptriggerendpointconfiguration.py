from typing import Optional

from office365.directory.extensions.customextensionendpointconfiguration import CustomExtensionEndpointConfiguration


class LogicAppTriggerEndpointConfiguration(CustomExtensionEndpointConfiguration):
    def __init__(
        self,
        logic_app_workflow_name: Optional[str] = None,
        resource_group_name: Optional[str] = None,
        subscription_id: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.logicAppWorkflowName = logic_app_workflow_name
        self.resourceGroupName = resource_group_name
        self.subscriptionId = subscription_id
        self.url = url

    @property
    def entity_type_name(self):
        return "microsoft.graph.LogicAppTriggerEndpointConfiguration"
