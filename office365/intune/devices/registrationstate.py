from enum import Enum


class DeviceRegistrationState(Enum):
    notRegistered = "0"
    registered = "2"
    revoked = "3"
    keyConflict = "4"
    approvalPending = "5"
    certificateReset = "6"
    notRegisteredPendingEnrollment = "7"
    unknown = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceRegistrationState"
