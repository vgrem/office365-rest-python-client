from __future__ import annotations

from office365.directory.identities.on_verified_id_claim_validation_handler import OnVerifiedIdClaimValidationHandler
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OnVerifiedIdClaimValidationListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnVerifiedIdClaimValidationHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnVerifiedIdClaimValidationHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnVerifiedIdClaimValidationListener"
