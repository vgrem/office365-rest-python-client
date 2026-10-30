from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.print.event import PrintEvent
    from office365.intune.print.task_definition import PrintTaskDefinition


class PrintTaskTrigger(Entity):
    @odata(name="event")
    @property
    def event(self) -> PrintEvent:
        """Gets the event property"""
        from office365.intune.print.event import PrintEvent

        return self.properties.get("event", PrintEvent.jobStarted)

    @odata(name="definition", navigation=True)
    @property
    def definition(self) -> PrintTaskDefinition:
        """Gets the definition property"""
        from office365.intune.print.task_definition import PrintTaskDefinition

        return self.properties.get(
            "definition", PrintTaskDefinition(self.context, ResourcePath("definition", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintTaskTrigger"
