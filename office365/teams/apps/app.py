from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.teams.apps.definition import TeamsAppDefinition


class TeamsApp(Entity):
    """Represents an app in the Microsoft Teams app catalog."""

    def __str__(self):
        return self.display_name or self.entity_type_name

    @property
    def display_name(self) -> Optional[str]:
        """The title of the TeamsApp."""
        return self.properties.get("displayName", None)

    @property
    def distribution_method(self) -> Optional[str]:
        """The title of the TeamsApp."""
        return self.properties.get("distributionMethod", None)

    @odata(name="appDefinitions")
    @property
    def app_definitions(self) -> EntityCollection[TeamsAppDefinition]:
        """The details for each version of the app."""
        return self.properties.get(
            "appDefinitions",
            EntityCollection(
                self.context,
                TeamsAppDefinition,
                ResourcePath("appDefinitions", self.resource_path),
            ),
        )
