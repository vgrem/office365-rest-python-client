from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class OnenoteOperationError(ClientValue):
    """An error from a failed OneNote operation.

    Args:
        message (str): The error message.
        code (str): The error code.
    """

    message: str | None = None
    code: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnenoteOperationError"
