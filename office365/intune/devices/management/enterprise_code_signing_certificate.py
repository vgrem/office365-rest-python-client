from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.certificates.status import CertificateStatus
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class EnterpriseCodeSigningCertificate(Entity):
    @odata(name="content")
    @property
    def content(self) -> Optional[bytes]:
        """Gets the content property"""
        return self.properties.get("content", None)

    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> Optional[datetime]:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="issuer")
    @property
    def issuer(self) -> Optional[str]:
        """Gets the issuer property"""
        return self.properties.get("issuer", None)

    @odata(name="issuerName")
    @property
    def issuer_name(self) -> Optional[str]:
        """Gets the issuerName property"""
        return self.properties.get("issuerName", None)

    @odata(name="status")
    @property
    def status(self) -> CertificateStatus:
        """Gets the status property"""
        return self.properties.get("status", CertificateStatus.notProvisioned)

    @odata(name="subject")
    @property
    def subject(self) -> Optional[str]:
        """Gets the subject property"""
        return self.properties.get("subject", None)

    @odata(name="subjectName")
    @property
    def subject_name(self) -> Optional[str]:
        """Gets the subjectName property"""
        return self.properties.get("subjectName", None)

    @odata(name="uploadDateTime")
    @property
    def upload_date_time(self) -> Optional[datetime]:
        """Gets the uploadDateTime property"""
        return self.properties.get("uploadDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EnterpriseCodeSigningCertificate"
