from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.security.ssl_certificate import SslCertificate
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.security.host import Host


class HostPort(Entity):
    @property
    def first_seen_date_time(self) -> datetime:
        """Gets the firstSeenDateTime property"""
        return self.properties.get("firstSeenDateTime", datetime.min)

    @property
    def last_scan_date_time(self) -> datetime:
        """Gets the lastScanDateTime property"""
        return self.properties.get("lastScanDateTime", datetime.min)

    @property
    def last_seen_date_time(self) -> datetime:
        """Gets the lastSeenDateTime property"""
        return self.properties.get("lastSeenDateTime", datetime.min)

    @property
    def port(self) -> Optional[int]:
        """Gets the port property"""
        return self.properties.get("port", None)

    @property
    def times_observed(self) -> Optional[int]:
        """Gets the timesObserved property"""
        return self.properties.get("timesObserved", None)

    @property
    def host(self) -> Host:
        """Gets the host property"""
        return self.properties.get("host", Host(self.context, ResourcePath("host", self.resource_path)))

    @odata(name="mostRecentSslCertificate")
    @property
    def most_recent_ssl_certificate(self) -> SslCertificate:
        """Gets the mostRecentSslCertificate property"""
        return self.properties.get(
            "mostRecentSslCertificate",
            SslCertificate(self.context, ResourcePath("mostRecentSslCertificate", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.HostPort"
