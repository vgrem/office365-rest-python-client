from __future__ import annotations

from office365.directory.authentication.attributecollection.method_load_start_handler import (  # noqa: E501
    OnAuthenticationMethodLoadStartHandler,
)
from office365.directory.authentication.conditions.event_listener import AuthenticationEventListener
from office365.runtime.types.odata_property import odata


class OnAuthenticationMethodLoadStartListener(AuthenticationEventListener):
    @odata(name="handler")
    @property
    def handler(self) -> OnAuthenticationMethodLoadStartHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnAuthenticationMethodLoadStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnAuthenticationMethodLoadStartListener"
