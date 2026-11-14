from __future__ import annotations

from typing import Optional

from office365.directory.domains.dns_record import DomainDnsRecord
from office365.runtime.types.odata_property import odata


class DomainDnsTxtRecord(DomainDnsRecord):
    @odata(name="text")
    @property
    def text(self) -> Optional[str]:
        """Gets the text property"""
        return self.properties.get("text", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DomainDnsTxtRecord"
