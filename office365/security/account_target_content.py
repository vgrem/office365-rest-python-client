from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.security.attacksimulations.account_target_content_type import (
    AccountTargetContentType,
)


class AccountTargetContent(ClientValue):
    type: AccountTargetContentType = AccountTargetContentType.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccountTargetContent"
