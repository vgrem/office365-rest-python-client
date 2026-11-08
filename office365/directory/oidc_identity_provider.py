from __future__ import annotations

from typing import Optional

from office365.directory.authentication.oidc_client_authentication import OidcClientAuthentication
from office365.directory.authentication.oidc_inbound_claim_mapping_override import OidcInboundClaimMappingOverride
from office365.directory.identities.providers.oidc_response_type import OidcResponseType
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OidcIdentityProvider(Entity):
    @odata(name="clientAuthentication")
    @property
    def client_authentication(self) -> OidcClientAuthentication:
        """Gets the clientAuthentication property"""
        return self.properties.get("clientAuthentication", OidcClientAuthentication())

    @odata(name="clientId")
    @property
    def client_id(self) -> Optional[str]:
        """Gets the clientId property"""
        return self.properties.get("clientId", None)

    @odata(name="inboundClaimMapping")
    @property
    def inbound_claim_mapping(self) -> OidcInboundClaimMappingOverride:
        """Gets the inboundClaimMapping property"""
        return self.properties.get("inboundClaimMapping", OidcInboundClaimMappingOverride())

    @odata(name="issuer")
    @property
    def issuer(self) -> Optional[str]:
        """Gets the issuer property"""
        return self.properties.get("issuer", None)

    @odata(name="responseType")
    @property
    def response_type(self) -> OidcResponseType:
        """Gets the responseType property"""
        return self.properties.get("responseType", OidcResponseType.code)

    @odata(name="scope")
    @property
    def scope(self) -> Optional[str]:
        """Gets the scope property"""
        return self.properties.get("scope", None)

    @odata(name="wellKnownEndpoint")
    @property
    def well_known_endpoint(self) -> Optional[str]:
        """Gets the wellKnownEndpoint property"""
        return self.properties.get("wellKnownEndpoint", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OidcIdentityProvider"
