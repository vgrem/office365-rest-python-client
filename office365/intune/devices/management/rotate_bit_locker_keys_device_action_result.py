from __future__ import annotations

from office365.intune.devices.management.action_result import DeviceActionResult


class RotateBitLockerKeysDeviceActionResult(DeviceActionResult):
    errorCode: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RotateBitLockerKeysDeviceActionResult"
