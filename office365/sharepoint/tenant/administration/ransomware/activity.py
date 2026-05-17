from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from typing import Optional


class TenantAdminRansomwareActivity(ClientValue):
    def __init__(
        self,
        activity_generated_on: Optional[datetime] = None,
        activity_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
        category: Optional[int] = None,
        classification: Optional[int] = None,
        created_time: Optional[datetime] = None,
        detection_source: Optional[str] = None,
        drive_id: Optional[str] = None,
        event_id: Optional[str] = None,
        first_activity: Optional[datetime] = None,
        impacted_asset_location: Optional[str] = None,
        impacted_assets: Optional[str] = None,
        impacted_assets_count: Optional[int] = None,
        impacted_assets_user_count: Optional[int] = None,
        impacted_doc_lib_name: Optional[str] = None,
        investigation_state: Optional[int] = None,
        last_activity: Optional[datetime] = None,
        last_updated_time: Optional[datetime] = None,
        processed_status: Optional[int] = None,
        ransomware_detection_reason: Optional[str] = None,
        ransomware_detection_score: Optional[float] = None,
        run_id: Optional[UUID] = None,
        site_id: Optional[UUID] = None,
        site_name: Optional[str] = None,
        site_owner: Optional[str] = None,
        site_type: Optional[int] = None,
        site_url: Optional[str] = None,
        status: Optional[int] = None,
        sync_status: Optional[int] = None,
        tag_id: Optional[str] = None,
        updated_by: Optional[str] = None,
        user_name: Optional[str] = None,
        web_id: Optional[UUID] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareActivity"
