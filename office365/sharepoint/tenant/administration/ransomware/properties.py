from datetime import datetime

from office365.runtime.client_value import ClientValue


class RansomwareProperties(ClientValue):
    def __init__(
        self,
        activity_generated_on: datetime = None,
        activity_id: str = None,
        category: int = None,
        detection_source: str = None,
        drive_id: str = None,
        first_activity: datetime = None,
        impacted_asset_location: str = None,
        impacted_assets_count: int = None,
        impacted_doc_lib_name: str = None,
        impacted_site_type: int = None,
        last_activity: datetime = None,
        processed_status: int = None,
        ransomware_detection_reason: str = None,
        ransomware_detection_score: float = None,
        run_id: str = None,
        site_label_id: str = None,
        site_label_name: str = None,
        site_name: str = None,
        site_owner_name: str = None,
        site_subscription_id: str = None,
        site_url: str = None,
        user_name: str = None,
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
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.RansomwareProperties"
