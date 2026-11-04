from __future__ import annotations

from dataclasses import field

from office365.outlook.mail.physical_address import PhysicalAddress
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class SslCertificateEntity(ClientValue):
    address: PhysicalAddress = field(default_factory=PhysicalAddress)
    alternateNames: StringCollection = field(default_factory=StringCollection)
    commonName: str | None = None
    email: str | None = None
    givenName: str | None = None
    organizationName: str | None = None
    organizationUnitName: str | None = None
    serialNumber: str | None = None
    surname: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.SslCertificateEntity"
