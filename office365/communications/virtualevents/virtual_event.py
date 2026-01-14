from typing import Optional

from office365.communications.virtualevents.presenter import VirtualEventPresenter
from office365.communications.virtualevents.session import VirtualEventSession
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.paths.resource_path import ResourcePath


class VirtualEvent(Entity):
    """Represents an abstract base type for a virtual event.
    Base type of virtualEventTownhall and virtualEventWebinar.
    """

    @property
    def description(self):
        # type: () -> Optional[str]
        """A description of the virtual event."""
        return self.properties.get("Description", ItemBody())

    @property
    def presenters(self):
        """The virtual event presenters."""
        return self.properties.get(
            "presenters",
            EntityCollection(
                self.context,
                VirtualEventPresenter,
                ResourcePath("presenters", self.resource_path),
            ),
        )

    @property
    def sessions(self):
        """The virtual event presenters."""
        return self.properties.get(
            "sessions",
            EntityCollection(
                self.context,
                VirtualEventSession,
                ResourcePath("sessions", self.resource_path),
            ),
        )
