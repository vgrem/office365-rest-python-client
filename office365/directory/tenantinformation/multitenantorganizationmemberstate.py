from enum import Enum


class MultiTenantOrganizationMemberState(Enum):
    pending = "0"
    active = "1"
    removed = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MultiTenantOrganizationMemberState"
