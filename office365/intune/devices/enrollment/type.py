from enum import Enum


class DeviceEnrollmentType(Enum):
    unknown = "0"
    userEnrollment = "1"
    deviceEnrollmentManager = "2"
    appleBulkWithUser = "3"
    appleBulkWithoutUser = "4"
    windowsAzureADJoin = "5"
    windowsBulkUserless = "6"
    windowsAutoEnrollment = "7"
    windowsBulkAzureDomainJoin = "8"
    windowsCoManagement = "9"
    windowsAzureADJoinUsingDeviceAuth = "10"
    appleUserEnrollment = "11"
    appleUserEnrollmentWithServiceAccount = "12"
    unknownFutureValue = "26"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceEnrollmentType"
