from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.permissions.identity import Identity
from office365.entity import Entity


class ApprovalStage(Entity):
    @property
    def assigned_to_me(self) -> Optional[bool]:
        """Gets the assignedToMe property"""
        return self.properties.get("assignedToMe", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def justification(self) -> Optional[str]:
        """Gets the justification property"""
        return self.properties.get("justification", None)

    @property
    def reviewed_by(self) -> Identity:
        """Gets the reviewedBy property"""
        return self.properties.get("reviewedBy", Identity())

    @property
    def reviewed_date_time(self) -> datetime:
        """Gets the reviewedDateTime property"""
        return self.properties.get("reviewedDateTime", datetime.min)

    @property
    def review_result(self) -> Optional[str]:
        """Gets the reviewResult property"""
        return self.properties.get("reviewResult", None)

    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApprovalStage"
