from enum import Enum


class MultiTenantOrganizationMemberRole(Enum):
    owner = "0"
    member = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MultiTenantOrganizationMemberRole"
