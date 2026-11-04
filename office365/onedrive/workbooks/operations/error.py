from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class WorkbookOperationError(ClientValue):
    """Represents an error from a failed workbook operation."""

    code: str | None = None
    innerError: str | None = None
    message: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookOperationError"
