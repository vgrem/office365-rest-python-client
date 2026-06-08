from __future__ import annotations

from office365.count_collection import CountCollection
from office365.directory.serviceprincipals.service_principal import ServicePrincipal
from office365.runtime.paths.appid import AppIdPath


class ServicePrincipalCollection(CountCollection[ServicePrincipal]):
    """Service Principal's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, ServicePrincipal, resource_path)

    def add(self, app_id: str) -> ServicePrincipal:
        """Create a new servicePrincipal object.

        Args:
            app_id (str): The unique identifier for the associated application
        """
        return super().add(appId=app_id)

    def get_by_app_id(self, app_id: str) -> ServicePrincipal:
        """Retrieves the service principal using appId.

        Args:
            app_id (str): appId is referred to as Application (Client) ID, respectively, in the Azure portal
        """
        return ServicePrincipal(self.context, AppIdPath(app_id, self.resource_path))

    def get_by_name(self, name: str) -> ServicePrincipal:
        """Retrieves the service principal using displayName."""
        return self.single(f"displayName eq '{name}'")
