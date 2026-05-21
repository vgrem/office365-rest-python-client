from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.mail.recipient import Recipient
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


@dataclass
class MessageRulePredicates(ClientValue):
    """Represents the set of conditions and exceptions that are available for a rule."""

    bodyContains: StringCollection = field(default_factory=StringCollection)
    bodyOrSubjectContains: StringCollection = field(default_factory=StringCollection)
    categories: StringCollection = field(default_factory=StringCollection)
    fromAddresses: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(Recipient))
    hasAttachments: bool | None = None
    headerContains: StringCollection = field(default_factory=StringCollection)
    importance: str | None = None
    isApprovalRequest: bool | None = None
