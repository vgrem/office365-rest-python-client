from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ResetPasscodeActionResult(ClientValue):
    errorCode: int | None = None
    passcode: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResetPasscodeActionResult"
