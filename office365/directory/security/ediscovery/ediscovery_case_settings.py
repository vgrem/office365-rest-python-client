from __future__ import annotations

from office365.directory.security.cases.reviewsetsettings import ReviewSetSettings
from office365.directory.security.cases.type import CaseType
from office365.entity import Entity


class EdiscoveryCaseSettings(Entity):
    @property
    def case_type(self) -> CaseType:
        """Gets the caseType property"""
        return self.properties.get("caseType", CaseType.standard)

    @property
    def review_set_settings(self) -> ReviewSetSettings:
        """Gets the reviewSetSettings property"""
        return self.properties.get("reviewSetSettings", ReviewSetSettings.none)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryCaseSettings"
