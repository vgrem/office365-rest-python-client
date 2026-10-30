from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.externalconnectors.activitytype import ExternalActivityType
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.externalconnectors.identity import Identity


class ExternalActivity(Entity):
    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @odata(name="type")
    @property
    def type_(self) -> ExternalActivityType:
        """Gets the type property"""
        return self.properties.get("type", ExternalActivityType.unknown)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ExternalActivity"

    @odata(name="performedBy", navigation=True)
    @property
    def performed_by(self) -> Identity:
        """Gets the performedBy property"""
        from office365.externalconnectors.identity import Identity

        return self.properties.get(
            "performedBy", Identity(self.context, ResourcePath("performedBy", self.resource_path))
        )
