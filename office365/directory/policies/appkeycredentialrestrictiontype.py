from enum import Enum


class AppKeyCredentialRestrictionType(Enum):
    asymmetricKeyLifetime = "0"
    unknownFutureValue = "99"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppKeyCredentialRestrictionType"
