from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.teams.apps.app import TeamsApp
from office365.teams.apps.definition import TeamsAppDefinition


class TeamsAppInstallation(Entity):
    """
    Represents a teamsApp installed in a team or the personal scope of a user. Any bots that are part of the app will
    become part of any team or user's personal scope that the app is added to.
    """

    @odata(name="teamsApp")
    @property
    def teams_app(self) -> TeamsApp:
        """The app that is installed."""
        return self.properties.get(
            "teamsApp",
            TeamsApp(self.context, ResourcePath("teamsApp", self.resource_path)),
        )

    @odata(name="teamsAppDefinition")
    @property
    def teams_app_definition(self) -> TeamsAppDefinition:
        """The details of this version of the app."""
        return self.properties.get(
            "teamsAppDefinition",
            TeamsAppDefinition(self.context, ResourcePath("teamsAppDefinition", self.resource_path)),
        )
