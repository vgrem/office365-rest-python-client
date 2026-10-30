from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_work_from_anywhere_device import (  # noqa: E501
        UserExperienceAnalyticsWorkFromAnywhereDevice,
    )


class UserExperienceAnalyticsWorkFromAnywhereMetric(Entity):
    @odata(name="metricDevices", navigation=True)
    @property
    def metric_devices(self) -> EntityCollection[UserExperienceAnalyticsWorkFromAnywhereDevice]:
        """Gets the metricDevices property"""
        from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_work_from_anywhere_device import (  # noqa: E501
            UserExperienceAnalyticsWorkFromAnywhereDevice,
        )

        return self.properties.get(
            "metricDevices",
            EntityCollection[UserExperienceAnalyticsWorkFromAnywhereDevice](
                self.context,
                UserExperienceAnalyticsWorkFromAnywhereDevice,
                ResourcePath("metricDevices", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsWorkFromAnywhereMetric"
