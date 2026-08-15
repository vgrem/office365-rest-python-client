from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.accessreview.history.status import AccessReviewHistoryStatus
from office365.entity import Entity


class AccessReviewHistoryInstance(Entity):
    @property
    def download_uri(self) -> Optional[str]:
        """Gets the downloadUri property"""
        return self.properties.get("downloadUri", None)

    @property
    def expiration_date_time(self) -> datetime:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @property
    def fulfilled_date_time(self) -> datetime:
        """Gets the fulfilledDateTime property"""
        return self.properties.get("fulfilledDateTime", datetime.min)

    @property
    def review_history_period_end_date_time(self) -> datetime:
        """Gets the reviewHistoryPeriodEndDateTime property"""
        return self.properties.get("reviewHistoryPeriodEndDateTime", datetime.min)

    @property
    def review_history_period_start_date_time(self) -> datetime:
        """Gets the reviewHistoryPeriodStartDateTime property"""
        return self.properties.get("reviewHistoryPeriodStartDateTime", datetime.min)

    @property
    def run_date_time(self) -> datetime:
        """Gets the runDateTime property"""
        return self.properties.get("runDateTime", datetime.min)

    @property
    def status(self) -> AccessReviewHistoryStatus:
        """Gets the status property"""
        return self.properties.get("status", AccessReviewHistoryStatus.done)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewHistoryInstance"
