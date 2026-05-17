from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class RansomwareProperties(ClientValue):
    def __init__(
        self,
        activity_generated_on: Optional[datetime] = None,
        activity_id: Optional[str] = None,
        category: Optional[int] = None,
        detection_source: Optional[str] = None,
        drive_id: Optional[str] = None,
        first_activity: Optional[datetime] = None,
        impacted_asset_location: Optional[str] = None,
        impacted_assets_count: Optional[int] = None,
        impacted_doc_lib_name: Optional[str] = None,
        impacted_site_type: Optional[int] = None,
        last_activity: Optional[datetime] = None,
        processed_status: Optional[int] = None,
        ransomware_detection_reason: Optional[str] = None,
        ransomware_detection_score: Optional[float] = None,
        run_id: Optional[str] = None,
        site_label_id: Optional[str] = None,
        site_label_name: Optional[str] = None,
        site_name: Optional[str] = None,
        site_owner_name: Optional[str] = None,
        site_subscription_id: Optional[str] = None,
        site_url: Optional[str] = None,
        user_name: Optional[str] = None,
    ):
        self.activityGeneratedOn = activity_generated_on
        self.activityId = activity_id
        self.category = category
        self.detectionSource = detection_source
        self.driveId = drive_id
        self.firstActivity = first_activity
        self.impactedAssetLocation = impacted_asset_location
        self.impactedAssetsCount = impacted_assets_count
        self.impactedDocLibName = impacted_doc_lib_name
        self.impactedSiteType = impacted_site_type
        self.lastActivity = last_activity
        self.processedStatus = processed_status
        self.ransomwareDetectionReason = ransomware_detection_reason
        self.ransomwareDetectionScore = ransomware_detection_score
        self.runId = run_id
        self.siteLabelId = site_label_id
        self.siteLabelName = site_label_name
        self.siteName = site_name
        self.siteOwnerName = site_owner_name
        self.siteSubscriptionId = site_subscription_id
        self.siteUrl = site_url
        self.userName = user_name

    " "

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.RansomwareProperties"
