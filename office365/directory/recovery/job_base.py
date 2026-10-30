from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.recovery.recovery_status import RecoveryStatus
from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.recovery.job_filtering_criteria_base import (
        RecoveryJobFilteringCriteriaBase,
    )


class RecoveryJobBase(Entity):
    @odata(name="filteringCriteria")
    @property
    def filtering_criteria(self) -> RecoveryJobFilteringCriteriaBase:
        """Gets the filteringCriteria property"""
        from office365.directory.recovery.job_filtering_criteria_base import (
            RecoveryJobFilteringCriteriaBase,
        )

        return self.properties.get("filteringCriteria", RecoveryJobFilteringCriteriaBase())

    @odata(name="jobCompletionDateTime")
    @property
    def job_completion_date_time(self) -> Optional[datetime]:
        """Gets the jobCompletionDateTime property"""
        return self.properties.get("jobCompletionDateTime", datetime.min)

    @odata(name="jobStartDateTime")
    @property
    def job_start_date_time(self) -> Optional[datetime]:
        """Gets the jobStartDateTime property"""
        return self.properties.get("jobStartDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> RecoveryStatus:
        """Gets the status property"""
        return self.properties.get("status", RecoveryStatus.initialized)

    @odata(name="targetStateDateTime")
    @property
    def target_state_date_time(self) -> Optional[datetime]:
        """Gets the targetStateDateTime property"""
        return self.properties.get("targetStateDateTime", datetime.min)

    @odata(name="totalChangedLinksCalculated")
    @property
    def total_changed_links_calculated(self) -> Optional[int]:
        """Gets the totalChangedLinksCalculated property"""
        return self.properties.get("totalChangedLinksCalculated", None)

    @odata(name="totalChangedObjectsCalculated")
    @property
    def total_changed_objects_calculated(self) -> Optional[int]:
        """Gets the totalChangedObjectsCalculated property"""
        return self.properties.get("totalChangedObjectsCalculated", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.entraRecoveryServices.RecoveryJobBase"
