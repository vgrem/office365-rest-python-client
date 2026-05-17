from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class TenantAdminRansomwareActivitiesOverview(ClientValue):
    def __init__(
        self,
        category_threshold_limit: Optional[int] = None,
        first_activity_time: Optional[datetime] = None,
        impacted_assets_count: Optional[int] = None,
        last_activity_time: Optional[datetime] = None,
        one_drive_activity_count: Optional[int] = None,
        share_point_activity_count: Optional[int] = None,
        total_activities_count: Optional[int] = None,
        total_high_volume_component_activity_detection_count: Optional[int] = None,
        unresolved_activities_count: Optional[int] = None,
        users_count: Optional[int] = None,
    ):
        self.categoryThresholdLimit = category_threshold_limit
        self.firstActivityTime = first_activity_time
        self.impactedAssetsCount = impacted_assets_count
        self.lastActivityTime = last_activity_time
        self.oneDriveActivityCount = one_drive_activity_count
        self.sharePointActivityCount = share_point_activity_count
        self.totalActivitiesCount = total_activities_count
        self.totalHighVolumeComponentActivityDetectionCount = total_high_volume_component_activity_detection_count
        self.unresolvedActivitiesCount = unresolved_activities_count
        self.usersCount = users_count

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareActivitiesOverview"
