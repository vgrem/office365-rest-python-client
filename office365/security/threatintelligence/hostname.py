from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.security.threatintelligence.hosts.host import Host


class Hostname(Host):
    @odata(name="registrant")
    @property
    def registrant(self) -> Optional[str]:
        """Gets the registrant property"""
        return self.properties.get("registrant", None)

    @odata(name="registrar")
    @property
    def registrar(self) -> Optional[str]:
        """Gets the registrar property"""
        return self.properties.get("registrar", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.Hostname"
