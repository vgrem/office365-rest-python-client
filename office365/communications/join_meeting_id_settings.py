from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class JoinMeetingIdSettings(ClientValue):
    isPasscodeRequired: bool | None = None
    joinMeetingId: str | None = None
    passcode: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.JoinMeetingIdSettings"
