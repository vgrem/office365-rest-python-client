from __future__ import annotations

from enum import Enum


class PasswordPolicy(Enum):
    none = "0"
    changePasswordPeriod = "1"
    charactersCombination = "2"
    passwordHistoryAndReuse = "4"
    passwordLengthLimit = "8"
    personalInformationUse = "16"
    unknownFutureValue = "32"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PasswordPolicy"
