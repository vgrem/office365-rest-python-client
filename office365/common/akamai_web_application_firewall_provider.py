from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class AkamaiWebApplicationFirewallProvider(Entity):
    @odata(name="accessToken")
    @property
    def access_token(self) -> Optional[str]:
        """Gets the accessToken property"""
        return self.properties.get("accessToken", None)

    @odata(name="clientSecret")
    @property
    def client_secret(self) -> Optional[str]:
        """Gets the clientSecret property"""
        return self.properties.get("clientSecret", None)

    @odata(name="clientToken")
    @property
    def client_token(self) -> Optional[str]:
        """Gets the clientToken property"""
        return self.properties.get("clientToken", None)

    @odata(name="hostPrefix")
    @property
    def host_prefix(self) -> Optional[str]:
        """Gets the hostPrefix property"""
        return self.properties.get("hostPrefix", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AkamaiWebApplicationFirewallProvider"
