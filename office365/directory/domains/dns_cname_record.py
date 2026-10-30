from __future__ import annotations

from typing import Optional

from office365.directory.domains.dns_record import DomainDnsRecord
from office365.runtime.types.odata_property import odata


class DomainDnsCnameRecord(DomainDnsRecord):
    """
    Represents a CNAME record added to the DNS zone file of a particular domain in the tenant.
    """

    @odata(name="canonicalName")
    @property
    def canonical_name(self) -> Optional[str]:
        """Gets the canonicalName property"""
        return self.properties.get("canonicalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DomainDnsCnameRecord"
