from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class IpAddress(Entity):
    @property
    def country_or_region(self) -> Optional[str]:
        """Gets the countryOrRegion property"""
        return self.properties.get("countryOrRegion", None)

    @property
    def hosting_provider(self) -> Optional[str]:
        """Gets the hostingProvider property"""
        return self.properties.get("hostingProvider", None)

    @property
    def netblock(self) -> Optional[str]:
        """Gets the netblock property"""
        return self.properties.get("netblock", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.IpAddress"
