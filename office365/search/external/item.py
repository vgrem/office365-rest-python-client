from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.externalconnectors.external_activity import ExternalActivity
from office365.runtime.paths.resource_path import ResourcePath


class ExternalItem(Entity):
    """An item added to a Microsoft Graph connection."""

    @property
    def activities(self) -> EntityCollection[ExternalActivity]:
        """Gets the activities property"""
        return self.properties.get(
            "activities",
            EntityCollection[ExternalActivity](
                self.context, ExternalActivity, ResourcePath("activities", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ExternalItem"
