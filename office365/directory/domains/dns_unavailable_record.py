from __future__ import annotations

from typing import Optional

from office365.directory.domains.dns_record import DomainDnsRecord
from office365.runtime.types.odata_property import odata


class DomainDnsUnavailableRecord(DomainDnsRecord):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DomainDnsUnavailableRecord"
