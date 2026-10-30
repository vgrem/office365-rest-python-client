from __future__ import annotations

from office365.directory.identities.on_token_issuance_start_return_claim import OnTokenIssuanceStartReturnClaim
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class OnTokenIssuanceStartCustomExtension(Entity):
    @odata(name="claimsForTokenConfiguration")
    @property
    def claims_for_token_configuration(self) -> ClientValueCollection[OnTokenIssuanceStartReturnClaim]:
        """Gets the claimsForTokenConfiguration property"""
        return self.properties.get(
            "claimsForTokenConfiguration",
            ClientValueCollection[OnTokenIssuanceStartReturnClaim](OnTokenIssuanceStartReturnClaim),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnTokenIssuanceStartCustomExtension"
