from enum import Enum


class MobileThreatPartnerTenantState(Enum):
    unavailable = "0"
    available = "1"
    enabled = "2"
    unresponsive = "3"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MobileThreatPartnerTenantState"
