from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.security.threatintelligence.host import Host

if TYPE_CHECKING:
    from office365.security.whois_contact import WhoisContact
    from office365.security.whois_nameserver import WhoisNameserver


class WhoisBaseRecord(Entity):
    @odata(name="domainStatus")
    @property
    def domain_status(self) -> Optional[str]:
        """Gets the domainStatus property"""
        return self.properties.get("domainStatus", None)

    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> datetime:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="firstSeenDateTime")
    @property
    def first_seen_date_time(self) -> datetime:
        """Gets the firstSeenDateTime property"""
        return self.properties.get("firstSeenDateTime", datetime.min)

    @odata(name="lastSeenDateTime")
    @property
    def last_seen_date_time(self) -> datetime:
        """Gets the lastSeenDateTime property"""
        return self.properties.get("lastSeenDateTime", datetime.min)

    @odata(name="lastUpdateDateTime")
    @property
    def last_update_date_time(self) -> datetime:
        """Gets the lastUpdateDateTime property"""
        return self.properties.get("lastUpdateDateTime", datetime.min)

    @odata(name="rawWhoisText")
    @property
    def raw_whois_text(self) -> Optional[str]:
        """Gets the rawWhoisText property"""
        return self.properties.get("rawWhoisText", None)

    @odata(name="registrationDateTime")
    @property
    def registration_date_time(self) -> datetime:
        """Gets the registrationDateTime property"""
        return self.properties.get("registrationDateTime", datetime.min)

    @odata(name="whoisServer")
    @property
    def whois_server(self) -> Optional[str]:
        """Gets the whoisServer property"""
        return self.properties.get("whoisServer", None)

    @odata(name="host", navigation=True)
    @property
    def host(self) -> Host:
        """Gets the host property"""
        return self.properties.get("host", Host(self.context, ResourcePath("host", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.WhoisBaseRecord"

    @odata(name="abuse")
    @property
    def abuse(self) -> WhoisContact:
        """Gets the abuse property"""
        from office365.security.whois_contact import WhoisContact

        return self.properties.get("abuse", WhoisContact())

    @odata(name="admin")
    @property
    def admin(self) -> WhoisContact:
        """Gets the admin property"""
        from office365.security.whois_contact import WhoisContact

        return self.properties.get("admin", WhoisContact())

    @odata(name="billing")
    @property
    def billing(self) -> WhoisContact:
        """Gets the billing property"""
        from office365.security.whois_contact import WhoisContact

        return self.properties.get("billing", WhoisContact())

    @odata(name="nameservers")
    @property
    def nameservers(self) -> ClientValueCollection[WhoisNameserver]:
        """Gets the nameservers property"""
        from office365.security.whois_nameserver import WhoisNameserver

        return self.properties.get("nameservers", ClientValueCollection[WhoisNameserver](WhoisNameserver))

    @odata(name="noc")
    @property
    def noc(self) -> WhoisContact:
        """Gets the noc property"""
        from office365.security.whois_contact import WhoisContact

        return self.properties.get("noc", WhoisContact())

    @odata(name="registrant")
    @property
    def registrant(self) -> WhoisContact:
        """Gets the registrant property"""
        from office365.security.whois_contact import WhoisContact

        return self.properties.get("registrant", WhoisContact())

    @odata(name="registrar")
    @property
    def registrar(self) -> WhoisContact:
        """Gets the registrar property"""
        from office365.security.whois_contact import WhoisContact

        return self.properties.get("registrar", WhoisContact())

    @odata(name="technical")
    @property
    def technical(self) -> WhoisContact:
        """Gets the technical property"""
        from office365.security.whois_contact import WhoisContact

        return self.properties.get("technical", WhoisContact())

    @odata(name="zone")
    @property
    def zone(self) -> WhoisContact:
        """Gets the zone property"""
        from office365.security.whois_contact import WhoisContact

        return self.properties.get("zone", WhoisContact())
