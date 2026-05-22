from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.mail.importance import Importance
from office365.outlook.mail.recipient import Recipient
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


@dataclass
class MessageRuleActions(ClientValue):
    """Represents the set of actions that are available to a rule."""

    assignCategories: StringCollection = field(default_factory=StringCollection)
    copyToFolder: str | None = None
    delete: bool | None = None
    forwardAsAttachmentTo: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(Recipient))
    forwardTo: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(Recipient))
    markAsRead: bool | None = None
    markImportance: Importance | None = None
    moveToFolder: str | None = None
    permanentDelete: bool | None = None
    redirectTo: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(Recipient))
    stopProcessingRules: bool | None = None
