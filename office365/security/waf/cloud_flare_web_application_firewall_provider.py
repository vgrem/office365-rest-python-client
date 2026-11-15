from __future__ import annotations

from typing import Optional

from office365.directory.identities.web_application_firewall_provider import WebApplicationFirewallProvider
from office365.runtime.types.odata_property import odata


class CloudFlareWebApplicationFirewallProvider(WebApplicationFirewallProvider):
    @odata(name="apiToken")
    @property
    def api_token(self) -> Optional[str]:
        """Gets the apiToken property"""
        return self.properties.get("apiToken", None)

    @odata(name="zoneId")
    @property
    def zone_id(self) -> Optional[str]:
        """Gets the zoneId property"""
        return self.properties.get("zoneId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudFlareWebApplicationFirewallProvider"
