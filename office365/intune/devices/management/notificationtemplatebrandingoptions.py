from enum import Enum


class NotificationTemplateBrandingOptions(Enum):
    none = "0"
    includeCompanyLogo = "1"
    includeCompanyName = "2"
    includeContactInformation = "4"
    includeCompanyPortalLink = "8"
    includeDeviceDetails = "16"
    unknownFutureValue = "32"

    @property
    def entity_type_name(self):
        return "microsoft.graph.NotificationTemplateBrandingOptions"
