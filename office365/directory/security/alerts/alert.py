from datetime import datetime
from typing import Optional

from office365.directory.security.alerts.classification import AlertClassification
from office365.directory.security.alerts.comment import AlertComment
from office365.directory.security.alerts.detectionsource import DetectionSource
from office365.directory.security.alerts.determination import AlertDetermination
from office365.directory.security.alerts.evidence import AlertEvidence
from office365.directory.security.alerts.history_state import AlertHistoryState
from office365.directory.security.alerts.severity import AlertSeverity
from office365.directory.security.alerts.status import AlertStatus
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


class Alert(Entity):
    """This resource corresponds to the latest generation of alerts in the Microsoft Graph security API,
    representing potential security issues within a customer's tenant that Microsoft 365 Defender,
    or a security provider integrated with Microsoft 365 Defender, has identified."""

    @property
    def activity_group_name(self) -> Optional[str]:
        """"""
        return self.properties.get("activityGroupName", None)

    @property
    def actor_display_name(self) -> Optional[str]:
        """The adversary or activity group that is associated with this alert."""
        return self.properties.get("actorDisplayName", None)

    @property
    def alert_policy_id(self) -> Optional[str]:
        return self.properties.get("alertPolicyId", None)

    @property
    def evidence(self):
        """Collection of evidence related to the alert."""
        return self.properties.get("evidence", ClientValueCollection(AlertEvidence))

    @property
    def history_states(self):
        """Collection of changes for the alert."""
        return self.properties.get("historyStates", ClientValueCollection(AlertHistoryState))

    @property
    def alert_web_url(self) -> Optional[str]:
        """Gets the alertWebUrl property"""
        return self.properties.get("alertWebUrl", None)

    @property
    def assigned_to(self) -> Optional[str]:
        """Gets the assignedTo property"""
        return self.properties.get("assignedTo", None)

    @property
    def categories(self) -> StringCollection:
        """Gets the categories property"""
        return self.properties.get("categories", StringCollection(None))

    @property
    def category(self) -> Optional[str]:
        """Gets the category property"""
        return self.properties.get("category", None)

    @property
    def classification(self) -> AlertClassification:
        """Gets the classification property"""
        return self.properties.get("classification", AlertClassification.unknown)

    @property
    def comments(self) -> ClientValueCollection[AlertComment]:
        """Gets the comments property"""
        return self.properties.get("comments", ClientValueCollection[AlertComment](AlertComment))

    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def detection_source(self) -> DetectionSource:
        """Gets the detectionSource property"""
        return self.properties.get("detectionSource", DetectionSource.unknown)

    @property
    def detector_id(self) -> Optional[str]:
        """Gets the detectorId property"""
        return self.properties.get("detectorId", None)

    @property
    def determination(self) -> AlertDetermination:
        """Gets the determination property"""
        return self.properties.get("determination", AlertDetermination.unknown)

    @property
    def first_activity_date_time(self) -> Optional[datetime]:
        """Gets the firstActivityDateTime property"""
        return self.properties.get("firstActivityDateTime", datetime.min)

    @property
    def incident_id(self) -> Optional[str]:
        """Gets the incidentId property"""
        return self.properties.get("incidentId", None)

    @property
    def incident_web_url(self) -> Optional[str]:
        """Gets the incidentWebUrl property"""
        return self.properties.get("incidentWebUrl", None)

    @property
    def last_activity_date_time(self) -> Optional[datetime]:
        """Gets the lastActivityDateTime property"""
        return self.properties.get("lastActivityDateTime", datetime.min)

    @property
    def last_update_date_time(self) -> Optional[datetime]:
        """Gets the lastUpdateDateTime property"""
        return self.properties.get("lastUpdateDateTime", datetime.min)

    @property
    def mitre_techniques(self) -> StringCollection:
        """Gets the mitreTechniques property"""
        return self.properties.get("mitreTechniques", StringCollection(None))

    @property
    def product_name(self) -> Optional[str]:
        """Gets the productName property"""
        return self.properties.get("productName", None)

    @property
    def provider_alert_id(self) -> Optional[str]:
        """Gets the providerAlertId property"""
        return self.properties.get("providerAlertId", None)

    @property
    def recommended_actions(self) -> Optional[str]:
        """Gets the recommendedActions property"""
        return self.properties.get("recommendedActions", None)

    @property
    def resolved_date_time(self) -> Optional[datetime]:
        """Gets the resolvedDateTime property"""
        return self.properties.get("resolvedDateTime", datetime.min)

    @property
    def severity(self) -> AlertSeverity:
        """Gets the severity property"""
        return self.properties.get("severity", AlertSeverity.unknown)

    @property
    def status(self) -> AlertStatus:
        """Gets the status property"""
        return self.properties.get("status", AlertStatus())

    @property
    def system_tags(self) -> StringCollection:
        """Gets the systemTags property"""
        return self.properties.get("systemTags", StringCollection())

    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @property
    def threat_display_name(self) -> Optional[str]:
        """Gets the threatDisplayName property"""
        return self.properties.get("threatDisplayName", None)

    @property
    def threat_family_name(self) -> Optional[str]:
        """Gets the threatFamilyName property"""
        return self.properties.get("threatFamilyName", None)

    @property
    def title(self) -> Optional[str]:
        """Gets the title property"""
        return self.properties.get("title", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.Alert"
