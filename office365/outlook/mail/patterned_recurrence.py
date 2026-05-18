from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.mail.recurrence_pattern import RecurrencePattern
from office365.outlook.mail.recurrence_range import RecurrenceRange
from office365.runtime.client_value import ClientValue


@dataclass
class PatternedRecurrence(ClientValue):
    """
    The recurrence pattern and range. This shared object is used to define the recurrence of the following objects:

        accessReviewScheduleDefinition objects in Azure AD access reviews APIs
        event objects in the calendar API
        unifiedRoleAssignmentScheduleRequest and unifiedRoleEligibilityScheduleRequest objects in PIM
        accessPackageAssignment objects in Azure AD entitlement management.
    """

    pattern: RecurrencePattern = field(default_factory=RecurrencePattern)
    range: RecurrenceRange = field(default_factory=RecurrenceRange)
