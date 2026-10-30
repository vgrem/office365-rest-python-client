from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identities.on_verified_id_claim_validation_handler import (
        OnVerifiedIdClaimValidationHandler,
    )


class OnVerifiedIdClaimValidationListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnVerifiedIdClaimValidationHandler:
        """Gets the handler property"""
        from office365.directory.identities.on_verified_id_claim_validation_handler import (
            OnVerifiedIdClaimValidationHandler,
        )

        return self.properties.get("handler", OnVerifiedIdClaimValidationHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnVerifiedIdClaimValidationListener"
