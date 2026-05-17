from enum import Enum


class PartnerTenantType(Enum):
    microsoftSupport = "1"
    syndicatePartner = "2"
    breadthPartner = "3"
    breadthPartnerDelegatedAdmin = "4"
    resellerPartnerDelegatedAdmin = "5"
    valueAddedResellerPartnerDelegatedAdmin = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PartnerTenantType"
