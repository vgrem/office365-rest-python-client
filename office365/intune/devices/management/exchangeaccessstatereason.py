from enum import Enum


class DeviceManagementExchangeAccessStateReason(Enum):
    none = "0"
    unknown = "1"
    exchangeGlobalRule = "2"
    exchangeIndividualRule = "3"
    exchangeDeviceRule = "4"
    exchangeUpgrade = "5"
    exchangeMailboxPolicy = "6"
    other = "7"
    compliant = "8"
    notCompliant = "9"
    notEnrolled = "10"
    unknownLocation = "12"
    mfaRequired = "13"
    azureADBlockDueToAccessPolicy = "14"
    compromisedPassword = "15"
    deviceNotKnownWithManagedApp = "16"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementExchangeAccessStateReason"
