from __future__ import annotations

from office365.directory.identities.on_token_issuance_start_handler import OnTokenIssuanceStartHandler
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OnTokenIssuanceStartListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnTokenIssuanceStartHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnTokenIssuanceStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnTokenIssuanceStartListener"
