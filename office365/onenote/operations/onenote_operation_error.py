from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class OnenoteOperationError(ClientValue):
    """An error from a failed OneNote operation.

    :param str message: The error message.
    :param str code: The error code.
    """

    message: str | None = None
    code: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnenoteOperationError"
