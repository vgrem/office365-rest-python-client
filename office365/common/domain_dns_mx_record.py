from __future__ import annotations

from typing import Optional

from office365.directory.domains.dns_record import DomainDnsRecord
from office365.runtime.types.odata_property import odata


class DomainDnsMxRecord(DomainDnsRecord):
    @odata(name="mailExchange")
    @property
    def mail_exchange(self) -> Optional[str]:
        """Gets the mailExchange property"""
        return self.properties.get("mailExchange", None)

    @odata(name="preference")
    @property
    def preference(self) -> Optional[int]:
        """Gets the preference property"""
        return self.properties.get("preference", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DomainDnsMxRecord"
