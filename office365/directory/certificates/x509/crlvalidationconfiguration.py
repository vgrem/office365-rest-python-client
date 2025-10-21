from office365.directory.certificates.x509.crlvalidationconfigurationstate import (
    X509CertificateCRLValidationConfigurationState,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class X509CertificateCRLValidationConfiguration(ClientValue):

    def __init__(
        self,
        exempted_certificate_authorities_subject_key_identifiers: StringCollection = None,
        state: X509CertificateCRLValidationConfigurationState = X509CertificateCRLValidationConfigurationState.none,
    ):
        self.exemptedCertificateAuthoritiesSubjectKeyIdentifiers = (
            exempted_certificate_authorities_subject_key_identifiers
        )
        self.state = state

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateCRLValidationConfiguration"
