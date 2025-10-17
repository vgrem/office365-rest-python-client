from enum import Enum


class DeviceEnrollmentFailureReason(Enum):
    unknown = "0"
    authentication = "1"
    authorization = "2"
    accountValidation = "3"
    userValidation = "4"
    deviceNotSupported = "5"
    inMaintenance = "6"
    badRequest = "7"
    featureNotSupported = "8"
    enrollmentRestrictionsEnforced = "9"
    clientDisconnected = "10"
    userAbandonment = "11"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceEnrollmentFailureReason"
