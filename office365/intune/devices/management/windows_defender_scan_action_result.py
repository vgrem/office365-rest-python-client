from __future__ import annotations

from office365.intune.devices.management.action_result import DeviceActionResult


class WindowsDefenderScanActionResult(DeviceActionResult):
    scanType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDefenderScanActionResult"
