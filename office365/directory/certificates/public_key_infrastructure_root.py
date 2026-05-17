from office365.directory.certificates.auth_pki import CertificateBasedAuthPki
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class PublicKeyInfrastructureRoot(Entity):
    """The collection of public key infrastructure instances over different Microsoft Entra features."""

    @property
    def certificate_based_auth_configurations(self):
        """The collection of public key infrastructure instances for the certificate-based authentication feature
        for users."""
        return self.properties.get(
            "certificateBasedAuthConfigurations",
            EntityCollection(
                self.context,
                CertificateBasedAuthPki,
                ResourcePath("certificateBasedAuthConfigurations", self.resource_path),
            ),
        )
