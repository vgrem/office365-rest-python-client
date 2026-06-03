from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.teams.apps.app import TeamsApp
from office365.teams.tabs.configuration import TeamsTabConfiguration


class TeamsTab(Entity):
    """
    A teamsTab is a tab that's pinned (attached) to a channel within a team.
    """

    @odata(name="teamsApp")
    @property
    def teams_app(self) -> TeamsApp:
        """The application that is linked to the tab. This cannot be changed after tab creation."""
        return self.properties.get(
            "teamsApp",
            TeamsApp(self.context, ResourcePath("teamsApp", self.resource_path)),
        )

    @property
    def configuration(self) -> TeamsTabConfiguration:
        """
        Container for custom settings applied to a tab. The tab is considered configured only once this property is set.
        """
        return self.properties.get("configuration", TeamsTabConfiguration())
