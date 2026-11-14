from __future__ import annotations

from typing import Optional

from office365.reports.print_usage import PrintUsage
from office365.runtime.types.odata_property import odata


class PrintUsageByUser(PrintUsage):
    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintUsageByUser"
