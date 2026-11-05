from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.expiration_pattern import (
    ExpirationPattern,
)
from office365.outlook.mail.patterned_recurrence import PatternedRecurrence
from office365.runtime.client_value import ClientValue


class RequestSchedule(ClientValue):
    expiration: ExpirationPattern = field(default_factory=ExpirationPattern)
    recurrence: PatternedRecurrence = field(default_factory=PatternedRecurrence)
    startDateTime: datetime | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RequestSchedule"
