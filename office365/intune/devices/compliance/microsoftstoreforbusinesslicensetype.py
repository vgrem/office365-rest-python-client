from enum import Enum


class MicrosoftStoreForBusinessLicenseType(Enum):
    offline = "0"
    online = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MicrosoftStoreForBusinessLicenseType"
