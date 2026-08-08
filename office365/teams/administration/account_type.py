from __future__ import annotations

from enum import Enum


class AccountType(Enum):
    user = "0"
    resourceAccount = "1"
    guest = "2"
    sfbOnPremUser = "3"
    unknown = "4"
    unknownFutureValue = "5"
    ineligibleUser = "6"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.AccountType"
