from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.security.retention_event import RetentionEvent


class TriggersRoot(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "microsoft.graph.security.triggersRoot"

    @odata(name="retentionEvents", navigation=True)
    @property
    def retention_events(self) -> EntityCollection[RetentionEvent]:
        """Gets the retentionEvents property"""
        from office365.security.retention_event import RetentionEvent

        return self.properties.get(
            "retentionEvents",
            EntityCollection[RetentionEvent](
                self.context, RetentionEvent, ResourcePath("retentionEvents", self.resource_path)
            ),
        )
