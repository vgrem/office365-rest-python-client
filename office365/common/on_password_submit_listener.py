from __future__ import annotations

from office365.directory.identities.on_password_submit_handler import OnPasswordSubmitHandler
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OnPasswordSubmitListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnPasswordSubmitHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnPasswordSubmitHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnPasswordSubmitListener"
