from enum import Enum


class CloudPcGalleryImageStatus(Enum):
    supported = "0"
    supportedWithWarning = "1"
    notSupported = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcGalleryImageStatus"
