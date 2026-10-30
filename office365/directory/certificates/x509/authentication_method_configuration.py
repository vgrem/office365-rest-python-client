from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.certificates.x509.authenticationmodeconfiguration import (  # noqa: E501
    X509CertificateAuthenticationModeConfiguration,
)
from office365.directory.certificates.x509.authority_scope import X509CertificateAuthorityScope
from office365.directory.certificates.x509.crlvalidationconfiguration import X509CertificateCRLValidationConfiguration
from office365.directory.certificates.x509.issuer_hints_configuration import X509CertificateIssuerHintsConfiguration
from office365.directory.certificates.x509.userbinding import X509CertificateUserBinding
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.authentication.methods.target import (
        AuthenticationMethodTarget,
    )


class X509CertificateAuthenticationMethodConfiguration(Entity):
    @odata(name="authenticationModeConfiguration")
    @property
    def authentication_mode_configuration(self) -> X509CertificateAuthenticationModeConfiguration:
        """Gets the authenticationModeConfiguration property"""
        return self.properties.get("authenticationModeConfiguration", X509CertificateAuthenticationModeConfiguration())

    @odata(name="certificateAuthorityScopes")
    @property
    def certificate_authority_scopes(self) -> ClientValueCollection[X509CertificateAuthorityScope]:
        """Gets the certificateAuthorityScopes property"""
        return self.properties.get(
            "certificateAuthorityScopes",
            ClientValueCollection[X509CertificateAuthorityScope](X509CertificateAuthorityScope),
        )

    @odata(name="certificateUserBindings")
    @property
    def certificate_user_bindings(self) -> ClientValueCollection[X509CertificateUserBinding]:
        """Gets the certificateUserBindings property"""
        return self.properties.get(
            "certificateUserBindings", ClientValueCollection[X509CertificateUserBinding](X509CertificateUserBinding)
        )

    @odata(name="crlValidationConfiguration")
    @property
    def crl_validation_configuration(self) -> X509CertificateCRLValidationConfiguration:
        """Gets the crlValidationConfiguration property"""
        return self.properties.get("crlValidationConfiguration", X509CertificateCRLValidationConfiguration())

    @odata(name="issuerHintsConfiguration")
    @property
    def issuer_hints_configuration(self) -> X509CertificateIssuerHintsConfiguration:
        """Gets the issuerHintsConfiguration property"""
        return self.properties.get("issuerHintsConfiguration", X509CertificateIssuerHintsConfiguration())

    @odata(name="includeTargets", navigation=True)
    @property
    def include_targets(self) -> EntityCollection[AuthenticationMethodTarget]:
        """Gets the includeTargets property"""
        from office365.directory.authentication.methods.target import (
            AuthenticationMethodTarget,
        )

        return self.properties.get(
            "includeTargets",
            EntityCollection[AuthenticationMethodTarget](
                self.context, AuthenticationMethodTarget, ResourcePath("includeTargets", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.X509CertificateAuthenticationMethodConfiguration"
