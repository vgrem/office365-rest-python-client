from __future__ import annotations

from dataclasses import field

from office365.intune.devices.management.action_result import DeviceActionResult
from office365.intune.devices.management.geo_location import DeviceGeoLocation


class LocateDeviceActionResult(DeviceActionResult):
    deviceLocation: DeviceGeoLocation = field(default_factory=DeviceGeoLocation)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LocateDeviceActionResult"
