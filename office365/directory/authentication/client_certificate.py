from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.configuration_base import (
    ApiAuthenticationConfigurationBase,
)
from office365.directory.certificates.pkcs12_information import (
    Pkcs12CertificateInformation,
)
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class ClientCertificateAuthentication(ApiAuthenticationConfigurationBase):
    """
    A type derived from apiAuthenticationConfigurationBase that is used to represent
    a Pkcs12-based client certificate authentication.
    This is used to retrieve the public properties of uploaded certificates.
    """

    certificateList: ClientValueCollection[Pkcs12CertificateInformation] = field(
        default_factory=lambda: ClientValueCollection(Pkcs12CertificateInformation)
    )
