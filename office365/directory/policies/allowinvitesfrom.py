from enum import Enum


class AllowInvitesFrom(Enum):
    none = "0"
    adminsAndGuestInviters = "1"
    adminsGuestInvitersAndAllMembers = "2"
    everyone = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AllowInvitesFrom"
