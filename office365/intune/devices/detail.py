from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class DeviceDetail(ClientValue):
    """Indicates device details associated with a device used for signing in. This includes information
    like device browser and operating system, and whether the device is Azure AD managed.

    Args:
        browser (str): Indicates the browser information of the used for signing in.
        device_id (str): Refers to the UniqueID of the device used for signing in.
        display_name (str): Refers to the name of the device used for signing in.
    """

    browser: str | None = None
    deviceId: str | None = None
    displayName: str | None = None
    isCompliant: bool | None = None
    isManaged: bool | None = None
    operatingSystem: str | None = None
    trustType: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceDetail"
