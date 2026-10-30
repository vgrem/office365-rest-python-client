from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identities.on_interactive_auth_flow_start_handler import (
        OnInteractiveAuthFlowStartHandler,
    )


class OnInteractiveAuthFlowStartListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnInteractiveAuthFlowStartHandler:
        """Gets the handler property"""
        from office365.directory.identities.on_interactive_auth_flow_start_handler import (
            OnInteractiveAuthFlowStartHandler,
        )

        return self.properties.get("handler", OnInteractiveAuthFlowStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnInteractiveAuthFlowStartListener"
