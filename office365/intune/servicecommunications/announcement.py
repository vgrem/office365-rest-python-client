from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.servicecommunications.health.health import ServiceHealth
from office365.intune.servicecommunications.issues.issue import ServiceHealthIssue
from office365.intune.servicecommunications.messages.update import ServiceUpdateMessage
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class ServiceAnnouncement(Entity):
    """A top-level container for service communications resources."""

    @odata(name="healthOverviews")
    @property
    def health_overviews(self) -> EntityCollection[ServiceHealth]:
        """Get the serviceHealth resources from the healthOverviews navigation property."""
        return self.properties.get(
            "healthOverviews",
            EntityCollection(
                self.context,
                ServiceHealth,
                ResourcePath("healthOverviews", self.resource_path),
            ),
        )

    @property
    def issues(self) -> EntityCollection[ServiceHealthIssue]:
        """Get the serviceHealthIssue resources from the issues navigation property."""
        return self.properties.get(
            "issues",
            EntityCollection(
                self.context,
                ServiceHealthIssue,
                ResourcePath("issues", self.resource_path),
            ),
        )

    @property
    def messages(self) -> EntityCollection[ServiceUpdateMessage]:
        """Get the serviceUpdateMessage resources from the messages navigation property."""
        return self.properties.get(
            "messages",
            EntityCollection(
                self.context,
                ServiceUpdateMessage,
                ResourcePath("messages", self.resource_path),
            ),
        )
