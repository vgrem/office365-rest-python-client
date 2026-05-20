from __future__ import annotations

from dataclasses import dataclass

from office365.directory.certificates.x509.crlvalidationconfigurationstate import (
    X509CertificateCRLValidationConfigurationState,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class X509CertificateCRLValidationConfiguration(ClientValue):
    exemptedCertificateAuthoritiesSubjectKeyIdentifiers: StringCollection | None = None
    state: X509CertificateCRLValidationConfigurationState = X509CertificateCRLValidationConfigurationState.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateCRLValidationConfiguration"
