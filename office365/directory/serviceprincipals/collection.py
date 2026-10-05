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

    def ensure(self, app_id: str) -> ServicePrincipal:
        """Return the service principal for ``app_id``, creating it when absent.

        Idempotent and deferred — resolve with ``execute_query()``. App-only
        (client-credentials) flows attach permissions and site grants to the
        service principal, not the application registration, so use this to make
        a freshly created app usable:

            client.service_principals.ensure(app.app_id).execute_query()

        Args:
            app_id: The application (client) ID of the app registration.

        Returns:
            ServicePrincipal: The existing or newly created service principal.
        """
        from office365.runtime.paths.v4.entity import EntityPath
        from office365.runtime.queries.create_entity import CreateEntityQuery
        from office365.runtime.queries.get_or_create import get_or_create

        return_type = self.create_typed_object({"appId": app_id}, EntityPath(None, self.resource_path))
        self.add_child(return_type)
        return get_or_create(
            find=lambda: self.get_by_app_id(app_id).get(),
            create_query=lambda: CreateEntityQuery(self, return_type, return_type),
            return_type=return_type,
        )
