from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.onedrive.operations.long_running import LongRunningOperation
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.runtime.types.public_error import PublicError


class RichLongRunningOperation(LongRunningOperation):
    """Represents the status of a long-running operation on a site or a list."""

    @odata(name="resourceId")
    @property
    def resource_id(self) -> Optional[str]:
        """The unique identifier for the result."""
        return self.properties.get("resourceId", None)

    @odata(name="error")
    @property
    def error(self) -> PublicError:
        """Gets the error property"""
        from office365.runtime.types.public_error import PublicError

        return self.properties.get("error", PublicError())

    @odata(name="percentageComplete")
    @property
    def percentage_complete(self) -> Optional[int]:
        """Gets the percentageComplete property"""
        return self.properties.get("percentageComplete", None)

    @odata(name="type")
    @property
    def type(self) -> Optional[str]:
        """Gets the type property"""
        return self.properties.get("type", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RichLongRunningOperation"
