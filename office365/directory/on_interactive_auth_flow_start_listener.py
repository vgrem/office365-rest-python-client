from __future__ import annotations

from office365.directory.authentication.conditions.event_listener import AuthenticationEventListener
from office365.directory.identities.on_interactive_auth_flow_start_handler import OnInteractiveAuthFlowStartHandler
from office365.runtime.types.odata_property import odata


class OnInteractiveAuthFlowStartListener(AuthenticationEventListener):
    @odata(name="handler")
    @property
    def handler(self) -> OnInteractiveAuthFlowStartHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnInteractiveAuthFlowStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnInteractiveAuthFlowStartListener"
