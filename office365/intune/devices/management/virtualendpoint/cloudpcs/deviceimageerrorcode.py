from enum import Enum


class CloudPcDeviceImageErrorCode(Enum):
    internalServerError = "0"
    sourceImageNotFound = "1"
    osVersionNotSupported = "2"
    sourceImageInvalid = "3"
    sourceImageNotGeneralized = "4"
    unknownFutureValue = "5"
    vmAlreadyAzureAdjoined = "6"
    paidSourceImageNotSupport = "7"
    sourceImageNotSupportCustomizeVMName = "8"
    sourceImageSizeExceedsLimitation = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcDeviceImageErrorCode"
