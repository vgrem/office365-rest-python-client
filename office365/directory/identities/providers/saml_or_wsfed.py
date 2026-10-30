from __future__ import annotations

from typing import Optional

from office365.directory.authentication.protocol import AuthenticationProtocol
from office365.directory.identities.providers.base import IdentityProviderBase
from office365.runtime.types.odata_property import odata


class SamlOrWsFedProvider(IdentityProviderBase):
    """An abstract type that provides configuration details for setting up a SAML or WS-Fed external domain-based
    identity provider (IdP)."""

    @odata(name="issuerUri")
    @property
    def issuer_uri(self) -> Optional[str]:
        """Issuer URI of the federation server."""
        return self.properties.get("issuerUri", None)

    @odata(name="metadataExchangeUri")
    @property
    def metadata_exchange_uri(self) -> Optional[str]:
        """Gets the metadataExchangeUri property"""
        return self.properties.get("metadataExchangeUri", None)

    @odata(name="passiveSignInUri")
    @property
    def passive_sign_in_uri(self) -> Optional[str]:
        """Gets the passiveSignInUri property"""
        return self.properties.get("passiveSignInUri", None)

    @odata(name="preferredAuthenticationProtocol")
    @property
    def preferred_authentication_protocol(self) -> AuthenticationProtocol:
        """Gets the preferredAuthenticationProtocol property"""
        return self.properties.get("preferredAuthenticationProtocol", AuthenticationProtocol.wsFed)

    @odata(name="signingCertificate")
    @property
    def signing_certificate(self) -> Optional[str]:
        """Gets the signingCertificate property"""
        return self.properties.get("signingCertificate", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SamlOrWsFedProvider"
