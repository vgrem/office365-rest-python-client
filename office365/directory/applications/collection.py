from typing import Any

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
