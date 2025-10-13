from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class AppPrincipal(Entity):

    @property
    def display_name(self) -> Optional[str]:
        """Gets the DisplayName property"""
        return self.properties.get("DisplayName", None)

    @property
    def endpoint_authorities(self) -> StringCollection:
        """Gets the EndpointAuthorities property"""
        return self.properties.get("EndpointAuthorities", StringCollection())

    @property
    def name_identifier(self) -> Optional[str]:
        """Gets the NameIdentifier property"""
        return self.properties.get("NameIdentifier", None)

    @property
    def redirect_addresses(self) -> StringCollection:
        """Gets the RedirectAddresses property"""
        return self.properties.get("RedirectAddresses", StringCollection())
