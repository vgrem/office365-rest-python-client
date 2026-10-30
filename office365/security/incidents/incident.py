from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.security.alerts.alert import Alert
from office365.security.alerts.comment import AlertComment
from office365.security.alerts.determination import AlertDetermination
from office365.security.alerts.severity import AlertSeverity
from office365.security.incidents.status import IncidentStatus


class Incident(Entity):
    """
    An incident in Microsoft 365 Defender is a collection of correlated alert instances and associated metadata
    that reflects the story of an attack in a tenant.

    Microsoft 365 services and apps create alerts when they detect a suspicious or malicious event or activity.
    Individual alerts provide valuable clues about a completed or ongoing attack. However, attacks typically employ
    various techniques against different types of entities, such as devices, users, and mailboxes. The result is
    multiple alerts for multiple entities in your tenant. Because piecing the individual alerts together to gain
    insight into an attack can be challenging and time-consuming, Microsoft 365 Defender automatically aggregates the
    alerts and their associated information into an incident.
    """

    @odata(name="assignedTo")
    @property
    def assigned_to(self) -> Optional[str]:
        """Owner of the incident, or null if no owner is assigned. Free editable text."""
        return self.properties.get("assignedTo", None)

    @odata(name="classification")
    @property
    def classification(self) -> Optional[str]:
        """The specification for the incident.
        Possible values are: unknown, falsePositive, truePositive, informationalExpectedActivity, unknownFutureValue.
        """
        return self.properties.get("classification", None)

    @odata(name="comments")
    @property
    def comments(self) -> ClientValueCollection[AlertComment]:
        """Array of comments created by the Security Operations (SecOps) team when the incident is managed."""
        return self.properties.get("comments", ClientValueCollection(AlertComment))

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> datetime:
        """Time when the incident was first created."""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="alerts", navigation=True)
    @property
    def alerts(self) -> EntityCollection[Alert]:
        """The list of related alerts. Supports $expand."""
        return self.properties.get(
            "alerts",
            EntityCollection(self.context, Alert, ResourcePath("alerts", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.incident"

    @odata(name="customTags")
    @property
    def custom_tags(self) -> StringCollection:
        """Gets the customTags property"""
        return self.properties.get("customTags", StringCollection())

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="determination")
    @property
    def determination(self) -> AlertDetermination:
        """Gets the determination property"""
        return self.properties.get("determination", AlertDetermination.unknown)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="incidentWebUrl")
    @property
    def incident_web_url(self) -> Optional[str]:
        """Gets the incidentWebUrl property"""
        return self.properties.get("incidentWebUrl", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> Optional[str]:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", None)

    @odata(name="lastUpdateDateTime")
    @property
    def last_update_date_time(self) -> Optional[datetime]:
        """Gets the lastUpdateDateTime property"""
        return self.properties.get("lastUpdateDateTime", datetime.min)

    @odata(name="priorityScore")
    @property
    def priority_score(self) -> Optional[int]:
        """Gets the priorityScore property"""
        return self.properties.get("priorityScore", None)

    @odata(name="redirectIncidentId")
    @property
    def redirect_incident_id(self) -> Optional[str]:
        """Gets the redirectIncidentId property"""
        return self.properties.get("redirectIncidentId", None)

    @odata(name="resolvingComment")
    @property
    def resolving_comment(self) -> Optional[str]:
        """Gets the resolvingComment property"""
        return self.properties.get("resolvingComment", None)

    @odata(name="severity")
    @property
    def severity(self) -> AlertSeverity:
        """Gets the severity property"""
        return self.properties.get("severity", AlertSeverity.unknown)

    @odata(name="status")
    @property
    def status(self) -> IncidentStatus:
        """Gets the status property"""
        return self.properties.get("status", IncidentStatus.active)

    @odata(name="summary")
    @property
    def summary(self) -> Optional[str]:
        """Gets the summary property"""
        return self.properties.get("summary", None)

    @odata(name="systemTags")
    @property
    def system_tags(self) -> StringCollection:
        """Gets the systemTags property"""
        return self.properties.get("systemTags", StringCollection())

    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)
