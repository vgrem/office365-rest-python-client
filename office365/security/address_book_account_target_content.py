from __future__ import annotations

from dataclasses import field

from office365.runtime.types.collections import StringCollection
from office365.security.account_target_content import AccountTargetContent


class AddressBookAccountTargetContent(AccountTargetContent):
    accountTargetEmails: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AddressBookAccountTargetContent"
