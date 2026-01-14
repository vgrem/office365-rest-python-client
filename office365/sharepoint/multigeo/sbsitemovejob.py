from datetime import datetime
from typing import Optional

from office365.sharepoint.entity import Entity


class SBSiteMoveJob(Entity):
    @property
    def is_site_in_read_only(self) -> Optional[bool]:
        """Gets the IsSiteInReadOnly property"""
        return self.properties.get("IsSiteInReadOnly", None)

    @property
    def job_phase_created_at(self) -> datetime:
        """Gets the JobPhaseCreatedAt property"""
        return self.properties.get("JobPhaseCreatedAt", None)

    @property
    def job_phase_finished_at(self) -> datetime:
        """Gets the JobPhaseFinishedAt property"""
        return self.properties.get("JobPhaseFinishedAt", None)

    @property
    def move_phase(self) -> Optional[str]:
        """Gets the MovePhase property"""
        return self.properties.get("MovePhase", None)

    @property
    def move_phase_state(self) -> Optional[str]:
        """Gets the MovePhaseState property"""
        return self.properties.get("MovePhaseState", None)

    @property
    def move_state_of_site(self) -> Optional[str]:
        """Gets the MoveStateOfSite property"""
        return self.properties.get("MoveStateOfSite", None)

    @property
    def task_step_name(self) -> Optional[str]:
        """Gets the TaskStepName property"""
        return self.properties.get("TaskStepName", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.SBSiteMoveJob"
