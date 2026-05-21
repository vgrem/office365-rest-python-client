from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class AlertEvidence(ClientValue):
    """The alertEvidence base type and its derived evidence types provide a means to organize and track rich data
    about each artifact involved in an alert."""

    createdDateTime: str | None = None
    detailedRoles: StringCollection = field(default_factory=StringCollection)
