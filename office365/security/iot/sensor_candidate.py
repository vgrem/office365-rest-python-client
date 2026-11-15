from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class SensorCandidate(Entity):
    @odata(name="computerDnsName")
    @property
    def computer_dns_name(self) -> Optional[str]:
        """Gets the computerDnsName property"""
        return self.properties.get("computerDnsName", None)

    @odata(name="domainName")
    @property
    def domain_name(self) -> Optional[str]:
        """Gets the domainName property"""
        return self.properties.get("domainName", None)

    @odata(name="lastSeenDateTime")
    @property
    def last_seen_date_time(self) -> datetime:
        """Gets the lastSeenDateTime property"""
        return self.properties.get("lastSeenDateTime", datetime.min)

    @odata(name="senseClientVersion")
    @property
    def sense_client_version(self) -> Optional[str]:
        """Gets the senseClientVersion property"""
        return self.properties.get("senseClientVersion", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.SensorCandidate"
