from typing import Any, Optional

from office365.count_collection import CountCollection
from office365.directory.applications.application import Application
from office365.runtime.paths.appid import AppIdPath


class ApplicationCollection(CountCollection[Application]):
    """DirectoryObject's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, Application, resource_path)

    def add(self, display_name: str, **kwargs: Any) -> Application:
        """Create a new application object.

        Args:
            display_name (str): Display name of the application.
        """
        props = {
            "displayName": display_name,
            **kwargs,
        }
        return super().add(**props)

    def get_by_app_id(self, app_id: str) -> Application:
        """Retrieves application by Application client identifier

        Args:
            app_id (str): Application client identifier
        """
        return Application(self.context, AppIdPath(app_id, self.resource_path))

    def ensure(
        self,
        display_name: str,
        app_id: Optional[str] = None,
        *,
        create_service_principal: bool = False,
        sign_in_audience: str = "AzureADMyOrg",
    ) -> Application:
        """Return an existing application or create a new one (idempotent setup).

        Use it to reuse or provision the app registration an app-only flow signs
        in with, without branching on "does it exist yet":

            app = client.applications.ensure("my-app", client_id).execute_query()

        Because Entra assigns the application (client) ID, the two modes are
        explicit: pass ``app_id`` to **reuse** that registration, or omit it to
        **create** one named ``display_name``.

        Deferred — resolve with ``execute_query()``.

        Args:
            display_name: Display name for a newly created application.
            app_id: Application (client) ID to reuse; when set, no app is created.
            create_service_principal: Also ensure the application's service
                principal exists (needed for app-only / client-credentials use).
                The service principal is created when absent and left untouched
                when it already exists.
            sign_in_audience: Audience for a newly created application.

        Returns:
            Application: The reused or newly created application.
        """
        if app_id is not None:
            return_type = self.get_by_app_id(app_id).get()
        else:
            return_type = self.add(display_name, signInAudience=sign_in_audience)

        if create_service_principal:
            return_type.after_execute(lambda app: self.context.service_principals.ensure(app.app_id))
        return return_type
