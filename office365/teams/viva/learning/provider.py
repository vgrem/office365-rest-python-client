from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.teams.viva.learning.content import LearningContent


class LearningProvider(Entity):
    """Represents an entity that holds the details about a learning provider in Viva learning."""

    @odata(name="learningContents")
    @property
    def learning_contents(self) -> EntityCollection[LearningContent]:
        """Learning catalog items for the provider."""
        return self.properties.get(
            "learningContents",
            EntityCollection(
                self.context,
                LearningContent,
                ResourcePath("learningContents", self.resource_path),
            ),
        )
