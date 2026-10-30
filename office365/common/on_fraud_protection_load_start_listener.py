from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identities.providers.on_fraud_protection_load_start_handler import (
        OnFraudProtectionLoadStartHandler,
    )


class OnFraudProtectionLoadStartListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnFraudProtectionLoadStartHandler:
        """Gets the handler property"""
        from office365.directory.identities.providers.on_fraud_protection_load_start_handler import (
            OnFraudProtectionLoadStartHandler,
        )

        return self.properties.get("handler", OnFraudProtectionLoadStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnFraudProtectionLoadStartListener"
