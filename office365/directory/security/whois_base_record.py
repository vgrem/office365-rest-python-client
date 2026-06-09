from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.security.host import Host
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class WhoisBaseRecord(Entity):
    @property
    def domain_status(self) -> Optional[str]:
        """Gets the domainStatus property"""
        return self.properties.get("domainStatus", None)

    @property
    def expiration_date_time(self) -> datetime:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @property
    def first_seen_date_time(self) -> datetime:
        """Gets the firstSeenDateTime property"""
        return self.properties.get("firstSeenDateTime", datetime.min)

    @property
    def last_seen_date_time(self) -> datetime:
        """Gets the lastSeenDateTime property"""
        return self.properties.get("lastSeenDateTime", datetime.min)

    @property
    def last_update_date_time(self) -> datetime:
        """Gets the lastUpdateDateTime property"""
        return self.properties.get("lastUpdateDateTime", datetime.min)

    @property
    def raw_whois_text(self) -> Optional[str]:
        """Gets the rawWhoisText property"""
        return self.properties.get("rawWhoisText", None)

    @property
    def registration_date_time(self) -> datetime:
        """Gets the registrationDateTime property"""
        return self.properties.get("registrationDateTime", datetime.min)

    @property
    def whois_server(self) -> Optional[str]:
        """Gets the whoisServer property"""
        return self.properties.get("whoisServer", None)

    @property
    def host(self) -> Host:
        """Gets the host property"""
        return self.properties.get("host", Host(self.context, ResourcePath("host", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.WhoisBaseRecord"
