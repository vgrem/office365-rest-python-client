from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class TenantAdminRansomwareActivity(ClientValue):

    def __init__(
        self,
        activity_generated_on: datetime = None,
        activity_id: str = None,
        assigned_to: str = None,
        category: int = None,
        classification: int = None,
        created_time: datetime = None,
        detection_source: str = None,
        drive_id: str = None,
        event_id: str = None,
        first_activity: datetime = None,
        impacted_asset_location: str = None,
        impacted_assets: str = None,
        impacted_assets_count: int = None,
        impacted_assets_user_count: int = None,
        impacted_doc_lib_name: str = None,
        investigation_state: int = None,
        last_activity: datetime = None,
        last_updated_time: datetime = None,
        processed_status: int = None,
        ransomware_detection_reason: str = None,
        ransomware_detection_score: float = None,
        run_id: UUID = None,
        site_id: UUID = None,
        site_name: str = None,
        site_owner: str = None,
        site_type: int = None,
        site_url: str = None,
        status: int = None,
        sync_status: int = None,
        tag_id: str = None,
        updated_by: str = None,
        user_name: str = None,
        web_id: UUID = None,
    ):
        self.activityGeneratedOn = activity_generated_on
        self.activityId = activity_id
        self.assignedTo = assigned_to
        self.category = category
        self.classification = classification
        self.createdTime = created_time
        self.detectionSource = detection_source
        self.driveId = drive_id
        self.eventId = event_id
        self.firstActivity = first_activity
        self.impactedAssetLocation = impacted_asset_location
        self.impactedAssets = impacted_assets
        self.impactedAssetsCount = impacted_assets_count
        self.impactedAssetsUserCount = impacted_assets_user_count
        self.impactedDocLibName = impacted_doc_lib_name
        self.investigationState = investigation_state
        self.lastActivity = last_activity
        self.lastUpdatedTime = last_updated_time
        self.processedStatus = processed_status
        self.ransomwareDetectionReason = ransomware_detection_reason
        self.RansomwareDetectionScore = ransomware_detection_score
        self.runId = run_id
        self.siteId = site_id
        self.siteName = site_name
        self.siteOwner = site_owner
        self.siteType = site_type
        self.siteUrl = site_url
        self.status = status
        self.syncStatus = sync_status
        self.tagId = tag_id
        self.updatedBy = updated_by
        self.userName = user_name
        self.webId = web_id

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareActivity"
