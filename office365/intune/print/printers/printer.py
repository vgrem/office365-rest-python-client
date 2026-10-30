from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity_collection import EntityCollection
from office365.intune.print.printers.base import PrinterBase
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.print.connectors.connector import PrintConnector
    from office365.intune.print.shares.share import PrinterShare
    from office365.intune.print.task_trigger import PrintTaskTrigger


class Printer(PrinterBase):
    """Represents a printer device that has been registered with the Universal Print service.
    Printer resources can be used to manage print jobs, printer settings, printer metadata and registration status.
    """

    @odata(name="hasPhysicalDevice")
    @property
    def has_physical_device(self) -> Optional[bool]:
        """Gets the hasPhysicalDevice property"""
        return self.properties.get("hasPhysicalDevice", None)

    @odata(name="isShared")
    @property
    def is_shared(self) -> Optional[bool]:
        """Gets the isShared property"""
        return self.properties.get("isShared", None)

    @odata(name="lastSeenDateTime")
    @property
    def last_seen_date_time(self) -> Optional[datetime]:
        """Gets the lastSeenDateTime property"""
        return self.properties.get("lastSeenDateTime", datetime.min)

    @odata(name="registeredDateTime")
    @property
    def registered_date_time(self) -> Optional[datetime]:
        """Gets the registeredDateTime property"""
        return self.properties.get("registeredDateTime", datetime.min)

    @odata(name="connectors", navigation=True)
    @property
    def connectors(self) -> EntityCollection[PrintConnector]:
        """Gets the connectors property"""
        from office365.intune.print.connectors.connector import PrintConnector

        return self.properties.get(
            "connectors",
            EntityCollection[PrintConnector](
                self.context, PrintConnector, ResourcePath("connectors", self.resource_path)
            ),
        )

    @odata(name="shares", navigation=True)
    @property
    def shares(self) -> EntityCollection[PrinterShare]:
        """Gets the shares property"""
        from office365.intune.print.shares.share import PrinterShare

        return self.properties.get(
            "shares",
            EntityCollection[PrinterShare](self.context, PrinterShare, ResourcePath("shares", self.resource_path)),
        )

    @odata(name="taskTriggers", navigation=True)
    @property
    def task_triggers(self) -> EntityCollection[PrintTaskTrigger]:
        """Gets the taskTriggers property"""
        from office365.intune.print.task_trigger import PrintTaskTrigger

        return self.properties.get(
            "taskTriggers",
            EntityCollection[PrintTaskTrigger](
                self.context, PrintTaskTrigger, ResourcePath("taskTriggers", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Printer"
