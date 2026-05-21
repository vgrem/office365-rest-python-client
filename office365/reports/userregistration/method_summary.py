from __future__ import annotations

from dataclasses import dataclass, field

from office365.reports.userregistration.method_count import UserRegistrationMethodCount
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class UserRegistrationMethodSummary(ClientValue):
    """Represents the summary of number of users registered for each authentication method."""

    totalUserCount: int | None = None
    userRegistrationMethodCounts: ClientValueCollection = field(
        default_factory=lambda: ClientValueCollection(UserRegistrationMethodCount)
    )
    userRoles: str | None = None
    userTypes: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserRegistrationMethodSummary"
