from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.teams.apps.app import TeamsApp


class AppCatalogs(Entity):
    """A container for apps from the Microsoft Teams app catalog"""

    @odata(name="teamsApps")
    @property
    def teams_apps(self) -> EntityCollection[TeamsApp]:
        """List apps from the Microsoft Teams app catalog."""
        return self.properties.get(
            "teamsApps",
            EntityCollection(self.context, TeamsApp, ResourcePath("teamsApps", self.resource_path)),
        )
