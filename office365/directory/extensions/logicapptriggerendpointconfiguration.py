from office365.directory.extensions.customextensionendpointconfiguration import CustomExtensionEndpointConfiguration


class LogicAppTriggerEndpointConfiguration(CustomExtensionEndpointConfiguration):

    def __init__(
        self,
        logic_app_workflow_name: str = None,
        resource_group_name: str = None,
        subscription_id: str = None,
        url: str = None,
    ):
        self.logicAppWorkflowName = logic_app_workflow_name
        self.resourceGroupName = resource_group_name
        self.subscriptionId = subscription_id
        self.url = url

    @property
    def entity_type_name(self):
        return "microsoft.graph.LogicAppTriggerEndpointConfiguration"
