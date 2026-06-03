from __future__ import annotations

from typing import Optional

from office365.directory.identitygovernance.privilegedaccess.schedule.requestactions import ScheduleRequestActions
from office365.entity import Entity


class PrivilegedAccessScheduleRequest(Entity):
    @property
    def action(self) -> ScheduleRequestActions:
        """Gets the action property"""
        return self.properties.get("action", ScheduleRequestActions.adminAssign)

    @property
    def is_validation_only(self) -> Optional[bool]:
        """Gets the isValidationOnly property"""
        return self.properties.get("isValidationOnly", None)

    @property
    def justification(self) -> Optional[str]:
        """Gets the justification property"""
        return self.properties.get("justification", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrivilegedAccessScheduleRequest"
