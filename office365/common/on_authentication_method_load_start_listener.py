from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.authentication.attributecollection.method_load_start_handler import (
        OnAuthenticationMethodLoadStartHandler,
    )


class OnAuthenticationMethodLoadStartListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnAuthenticationMethodLoadStartHandler:
        """Gets the handler property"""
        from office365.directory.authentication.attributecollection.method_load_start_handler import (
            OnAuthenticationMethodLoadStartHandler,
        )

        return self.properties.get("handler", OnAuthenticationMethodLoadStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnAuthenticationMethodLoadStartListener"
