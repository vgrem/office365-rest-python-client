from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.print.printers.capabilities import PrinterCapabilities
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.print.job import PrintJob
    from office365.intune.print.printers.defaults import PrinterDefaults
    from office365.intune.print.printers.location import PrinterLocation
    from office365.intune.print.printers.status import PrinterStatus


class PrinterBase(Entity):
    """Represents a base type for printer and printerShare entity types."""

    @property
    def capabilities(self):
        """The capabilities of the printer/printerShare."""
        return self.properties.get("", PrinterCapabilities())

    @odata(name="defaults")
    @property
    def defaults(self) -> PrinterDefaults:
        """Gets the defaults property"""
        from office365.intune.print.printers.defaults import PrinterDefaults

        return self.properties.get("defaults", PrinterDefaults())

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="isAcceptingJobs")
    @property
    def is_accepting_jobs(self) -> Optional[bool]:
        """Gets the isAcceptingJobs property"""
        return self.properties.get("isAcceptingJobs", None)

    @odata(name="location")
    @property
    def location(self) -> PrinterLocation:
        """Gets the location property"""
        from office365.intune.print.printers.location import PrinterLocation

        return self.properties.get("location", PrinterLocation())

    @odata(name="manufacturer")
    @property
    def manufacturer(self) -> Optional[str]:
        """Gets the manufacturer property"""
        return self.properties.get("manufacturer", None)

    @odata(name="model")
    @property
    def model(self) -> Optional[str]:
        """Gets the model property"""
        return self.properties.get("model", None)

    @odata(name="status")
    @property
    def status(self) -> PrinterStatus:
        """Gets the status property"""
        from office365.intune.print.printers.status import PrinterStatus

        return self.properties.get("status", PrinterStatus())

    @odata(name="jobs", navigation=True)
    @property
    def jobs(self) -> EntityCollection[PrintJob]:
        """Gets the jobs property"""
        from office365.intune.print.job import PrintJob

        return self.properties.get(
            "jobs", EntityCollection[PrintJob](self.context, PrintJob, ResourcePath("jobs", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrinterBase"
