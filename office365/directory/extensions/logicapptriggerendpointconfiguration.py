from __future__ import annotations

from office365.directory.extensions.custom.customextensionendpointconfiguration import CustomExtensionEndpointConfiguration


class LogicAppTriggerEndpointConfiguration(CustomExtensionEndpointConfiguration):
    logicAppWorkflowName: str | None = None
    resourceGroupName: str | None = None
    subscriptionId: str | None = None
    url: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.LogicAppTriggerEndpointConfiguration"
