from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.teams.viva.learning.courses.status import CourseStatus


class LearningCourseActivity(Entity):
    """Represents the activities that are part of an employee learning course."""

    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> Optional[datetime]:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="completionPercentage")
    @property
    def completion_percentage(self) -> Optional[int]:
        """Gets the completionPercentage property"""
        return self.properties.get("completionPercentage", None)

    @odata(name="externalcourseActivityId")
    @property
    def externalcourse_activity_id(self) -> Optional[str]:
        """Gets the externalcourseActivityId property"""
        return self.properties.get("externalcourseActivityId", None)

    @odata(name="learnerUserId")
    @property
    def learner_user_id(self) -> Optional[str]:
        """Gets the learnerUserId property"""
        return self.properties.get("learnerUserId", None)

    @odata(name="learningContentId")
    @property
    def learning_content_id(self) -> Optional[str]:
        """Gets the learningContentId property"""
        return self.properties.get("learningContentId", None)

    @odata(name="learningProviderId")
    @property
    def learning_provider_id(self) -> Optional[str]:
        """Gets the learningProviderId property"""
        return self.properties.get("learningProviderId", None)

    @odata(name="status")
    @property
    def status(self) -> CourseStatus:
        """Gets the status property"""
        return self.properties.get("status", CourseStatus.notStarted)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LearningCourseActivity"
