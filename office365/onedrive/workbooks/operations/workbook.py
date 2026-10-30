from typing import Optional

from office365.entity import Entity
from office365.onedrive.workbooks.operations.error import WorkbookOperationError
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata


class WorkbookOperation(PollableOperation, Entity):
    """Represents the status of a long-running workbook operation"""

    @odata(name="error")
    @property
    def error(self):
        """The error returned by the operation."""
        return self.properties.get("error", WorkbookOperationError())

    @odata(name="resourceLocation")
    @property
    def resource_location(self) -> Optional[str]:
        """The resource URI for the result."""
        return self.properties.get("resourceLocation", None)

    @odata(name="status")
    @property
    def status(self) -> Optional[str]:
        """The current status of the operation. Possible values are: NotStarted, Running, Completed, Failed."""
        return self.properties.get("status", None)
