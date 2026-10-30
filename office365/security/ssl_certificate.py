from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.security.ssl_certificate_entity import SslCertificateEntity

if TYPE_CHECKING:
    from office365.security.threatintelligence.host import Host


class SslCertificate(Entity):
    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> datetime:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="fingerprint")
    @property
    def fingerprint(self) -> Optional[str]:
        """Gets the fingerprint property"""
        return self.properties.get("fingerprint", None)

    @odata(name="firstSeenDateTime")
    @property
    def first_seen_date_time(self) -> datetime:
        """Gets the firstSeenDateTime property"""
        return self.properties.get("firstSeenDateTime", datetime.min)

    @odata(name="issueDateTime")
    @property
    def issue_date_time(self) -> datetime:
        """Gets the issueDateTime property"""
        return self.properties.get("issueDateTime", datetime.min)

    @odata(name="lastSeenDateTime")
    @property
    def last_seen_date_time(self) -> datetime:
        """Gets the lastSeenDateTime property"""
        return self.properties.get("lastSeenDateTime", datetime.min)

    @odata(name="serialNumber")
    @property
    def serial_number(self) -> Optional[str]:
        """Gets the serialNumber property"""
        return self.properties.get("serialNumber", None)

    @odata(name="sha1")
    @property
    def sha1(self) -> Optional[str]:
        """Gets the sha1 property"""
        return self.properties.get("sha1", None)

    @odata(name="relatedHosts", navigation=True)
    @property
    def related_hosts(self) -> EntityCollection[Host]:
        """Gets the relatedHosts property"""
        return self.properties.get(
            "relatedHosts", EntityCollection[Host](self.context, Host, ResourcePath("relatedHosts", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.SslCertificate"

    @odata(name="issuer")
    @property
    def issuer(self) -> SslCertificateEntity:
        """Gets the issuer property"""
        return self.properties.get("issuer", SslCertificateEntity())

    @odata(name="subject")
    @property
    def subject(self) -> SslCertificateEntity:
        """Gets the subject property"""
        return self.properties.get("subject", SslCertificateEntity())
