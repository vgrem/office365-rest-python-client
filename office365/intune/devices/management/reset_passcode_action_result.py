from __future__ import annotations

from office365.intune.devices.management.action_result import DeviceActionResult


class ResetPasscodeActionResult(DeviceActionResult):
    errorCode: int | None = None
    passcode: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResetPasscodeActionResult"
