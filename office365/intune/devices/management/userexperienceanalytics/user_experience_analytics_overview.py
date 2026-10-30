from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_insight import (
        UserExperienceAnalyticsInsight,
    )


class UserExperienceAnalyticsOverview(Entity):
    @odata(name="insights")
    @property
    def insights(self) -> ClientValueCollection[UserExperienceAnalyticsInsight]:
        """Gets the insights property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_insight import (
            UserExperienceAnalyticsInsight,
        )

        return self.properties.get(
            "insights", ClientValueCollection[UserExperienceAnalyticsInsight](UserExperienceAnalyticsInsight)
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsOverview"
