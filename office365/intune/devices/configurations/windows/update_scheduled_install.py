from __future__ import annotations

from datetime import time

from office365.intune.devices.configurations.windows.weeklyschedule import (
    WeeklySchedule,
)
from office365.runtime.client_value import ClientValue


class WindowsUpdateScheduledInstall(ClientValue):
    scheduledInstallDay: WeeklySchedule = WeeklySchedule.userDefined
    scheduledInstallTime: time | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsUpdateScheduledInstall"
