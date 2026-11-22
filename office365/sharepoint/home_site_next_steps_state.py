from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class HomeSiteNextStepsState(Entity):
    @odata(name="firstNudgeCompleted")
    @property
    def first_nudge_completed(self) -> Optional[bool]:
        """Gets the firstNudgeCompleted property"""
        return self.properties.get("firstNudgeCompleted", None)

    @odata(name="firstNudgeCompletedUtc")
    @property
    def first_nudge_completed_utc(self) -> Optional[str]:
        """Gets the firstNudgeCompletedUtc property"""
        return self.properties.get("firstNudgeCompletedUtc", None)

    @odata(name="secondNudgeCompleted")
    @property
    def second_nudge_completed(self) -> Optional[bool]:
        """Gets the secondNudgeCompleted property"""
        return self.properties.get("secondNudgeCompleted", None)
