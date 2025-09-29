from typing import Optional

from office365.runtime.paths.v3.static import StaticPath
from office365.sharepoint.entity import Entity


class ConnectionSettings(Entity):
    """The ConnectionSettings contains information about an endpoint (4) that can be used to connect to it."""

    def __init__(self, context, resource_path=None):
        if resource_path is None:
            resource_path = StaticPath(
                "Microsoft.BusinessData.Infrastructure.SecureStore.ConnectionSettings"
            )
        super().__init__(context, resource_path)

    @property
    def authentication_mode(self) -> Optional[str]:
        """The authentication mode used by the endpoint"""
        return self.properties.get("AuthenticationMode", None)

    @property
    def parent_name(self) -> Optional[str]:
        """The unique name used to identify the parent of the endpoint"""
        return self.properties.get("parentName", None)

    @property
    def entity_type_name(self):
        return "Microsoft.BusinessData.Infrastructure.SecureStore.ConnectionSettings"
