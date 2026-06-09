from __future__ import annotations

from datetime import datetime

from office365.directory.security.host import Host
from office365.directory.security.ssl_certificate import SslCertificate
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class HostSslCertificate(Entity):
    @property
    def first_seen_date_time(self) -> datetime:
        """Gets the firstSeenDateTime property"""
        return self.properties.get("firstSeenDateTime", datetime.min)

    @property
    def last_seen_date_time(self) -> datetime:
        """Gets the lastSeenDateTime property"""
        return self.properties.get("lastSeenDateTime", datetime.min)

    @property
    def host(self) -> Host:
        """Gets the host property"""
        return self.properties.get("host", Host(self.context, ResourcePath("host", self.resource_path)))

    @property
    def ssl_certificate(self) -> SslCertificate:
        """Gets the sslCertificate property"""
        return self.properties.get(
            "sslCertificate", SslCertificate(self.context, ResourcePath("sslCertificate", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.HostSslCertificate"
