from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.certificates.authoritytype import CertificateAuthorityType


class CertificateAuthorityDetail(Entity):
    @odata(name="certificate")
    @property
    def certificate(self) -> Optional[bytes]:
        """Gets the certificate property"""
        return self.properties.get("certificate", None)

    @odata(name="certificateAuthorityType")
    @property
    def certificate_authority_type(self) -> CertificateAuthorityType:
        """Gets the certificateAuthorityType property"""
        from office365.directory.certificates.authoritytype import (
            CertificateAuthorityType,
        )

        return self.properties.get("certificateAuthorityType", CertificateAuthorityType.root)

    @odata(name="certificateRevocationListUrl")
    @property
    def certificate_revocation_list_url(self) -> Optional[str]:
        """Gets the certificateRevocationListUrl property"""
        return self.properties.get("certificateRevocationListUrl", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="deltaCertificateRevocationListUrl")
    @property
    def delta_certificate_revocation_list_url(self) -> Optional[str]:
        """Gets the deltaCertificateRevocationListUrl property"""
        return self.properties.get("deltaCertificateRevocationListUrl", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> Optional[datetime]:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="isIssuerHintEnabled")
    @property
    def is_issuer_hint_enabled(self) -> Optional[bool]:
        """Gets the isIssuerHintEnabled property"""
        return self.properties.get("isIssuerHintEnabled", None)

    @odata(name="issuer")
    @property
    def issuer(self) -> Optional[str]:
        """Gets the issuer property"""
        return self.properties.get("issuer", None)

    @odata(name="issuerSubjectKeyIdentifier")
    @property
    def issuer_subject_key_identifier(self) -> Optional[str]:
        """Gets the issuerSubjectKeyIdentifier property"""
        return self.properties.get("issuerSubjectKeyIdentifier", None)

    @odata(name="thumbprint")
    @property
    def thumbprint(self) -> Optional[str]:
        """Gets the thumbprint property"""
        return self.properties.get("thumbprint", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CertificateAuthorityDetail"
