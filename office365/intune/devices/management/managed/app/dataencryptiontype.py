from enum import Enum


class ManagedAppDataEncryptionType(Enum):
    useDeviceSettings = "0"
    afterDeviceRestart = "1"
    whenDeviceLockedExceptOpenFiles = "2"
    whenDeviceLocked = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagedAppDataEncryptionType"
