from __future__ import annotations

from office365.directory.identities.providers.on_fraud_protection_load_start_handler import (  # noqa: E501
    OnFraudProtectionLoadStartHandler,
)
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OnFraudProtectionLoadStartListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnFraudProtectionLoadStartHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnFraudProtectionLoadStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnFraudProtectionLoadStartListener"
